import asyncio
import hmac
import json
import os
import re
import time
import traceback
import unicodedata
from pathlib import Path
from typing import Any, NamedTuple, Optional

import numpy as np
import onnxruntime as ort
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from tokenizers import Tokenizer

import audit

MODEL_DIR = Path(__file__).parent / "render_model"
MODEL_PATH = MODEL_DIR / "model_quantized.onnx"
AUDITED_PATHS = {"/predict"}  # health checks on "/" are not logged
REQUEST_TIMEOUT_S = 5.0  # /predict requests slower than this get a 504 (capstone criterion 3/4)
MAX_TEST_DELAY_S = 30.0  # upper bound for the X-Test-Delay hook
MAX_BODY_BYTES = 32 * 512  # larger request bodies are rejected unparsed
MAX_TEXT_CHARS = 1200  # the model only reads 256 tokens (~1.5k chars);
MAX_TOPIC_CHARS = 200
MAX_LOGGED_CHARS = 1000  # rejected input is truncated in the audit log

app = FastAPI()

audit.configure_model(
    name="takemeter-onnx",
    version=audit.file_fingerprint(MODEL_PATH),
    quantized=True,
)

# Load tokenizer and ONNX session once at startup
tokenizer = Tokenizer.from_file(str(MODEL_DIR / "tokenizer.json"))
tokenizer.enable_truncation(max_length=256)
tokenizer.enable_padding(pad_id=0, pad_token="[PAD]")

# Restrict threads to prevent memory spikes on Render's free tier
sess_options = ort.SessionOptions()
sess_options.intra_op_num_threads = 1
sess_options.inter_op_num_threads = 1

session = ort.InferenceSession(
    str(MODEL_PATH),
    sess_options=sess_options,
    providers=["CPUExecutionProvider"],
)

# Label order must match training. Read it from the exported model's
# config.json (written from id2label during training);
# fall back to the notebook's LABELS order.
try:
    with open(MODEL_DIR / "config.json", encoding="utf-8") as f:
        LABELS = {int(k): v for k, v in json.load(f)["id2label"].items()}
except (FileNotFoundError, KeyError):
    LABELS = {0: "fluff", 1: "substantive", 2: "derailing"}

INPUT_NAMES = {i.name for i in session.get_inputs()}


ALLOWED_KEYS = {"text", "topic"}
# Characters that render blank but are not stripped by str.strip() (Hangul fillers, braille blank).
INVISIBLE_CHARS = {chr(0x115F), chr(0x1160), chr(0x3164), chr(0xFFA0), chr(0x2800)}
ALLOWED_CONTROL_CHARS = {chr(9), chr(10), chr(13)}  # tab, newline, carriage return
HTML_TAG_RE = re.compile(r"</?\s*[a-zA-Z][^>]*>")


class TextRequest(NamedTuple):
    text: str
    topic: Optional[str]


def _reject(request: Request, reason: str, text: Any = None, topic: Any = None) -> HTTPException:
    """Record why a request was refused (and a bounded copy of its input) for the audit log."""
    audit_details = request.state.audit
    audit_details["reason"] = reason
    for key, value in (("input_text", text), ("input_topic", topic)):
        if isinstance(value, str):
            # backslashreplace keeps lone surrogates from crashing the UTF-8 log write
            audit_details[key] = value[:MAX_LOGGED_CHARS].encode("utf-8", "backslashreplace").decode("utf-8")
    return HTTPException(status_code=400, detail=reason)


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict:
    keys = [k for k, _ in pairs]
    dupes = sorted({k for k in keys if keys.count(k) > 1})
    if dupes:
        raise ValueError(f"duplicate key(s): {', '.join(dupes)}")
    return dict(pairs)


def _field_problem(name: str, value: str, max_chars: int) -> Optional[str]:
    if len(value) > max_chars:
        return f"{name} too long ({len(value)} chars, max {max_chars})"
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return f"{name} contains invalid unicode (lone surrogate)"
    if any(unicodedata.category(c) == "Cc" and c not in ALLOWED_CONTROL_CHARS for c in value):
        return f"{name} contains control characters"
    if HTML_TAG_RE.search(value):
        return f"{name} contains markup"
    return None


async def parse_body(request: Request) -> TextRequest:
    """Strictly validate the /predict body. Every failure is a 400 and is audit-logged."""
    raw = await request.body()
    if len(raw) > MAX_BODY_BYTES:
        raise _reject(request, f"request body too large ({len(raw)} bytes, max {MAX_BODY_BYTES})")
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys)
    except UnicodeDecodeError:
        raise _reject(request, "body is not valid UTF-8")
    except ValueError as exc:  # JSONDecodeError and duplicate keys
        raise _reject(request, f"invalid JSON: {exc}")
    if not isinstance(data, dict):
        raise _reject(request, "body must be a JSON object")
    unknown = sorted(set(data) - ALLOWED_KEYS)
    if unknown:
        raise _reject(request, f"unknown field(s): {', '.join(unknown)}", data.get("text"), data.get("topic"))

    text, topic = data.get("text"), data.get("topic")
    if not isinstance(text, str):
        raise _reject(request, "text is required and must be a string", None, topic)
    if topic is not None and not isinstance(topic, str):
        raise _reject(request, "topic must be a string or null", text)

    for name, value, limit in (("text", text, MAX_TEXT_CHARS), ("topic", topic, MAX_TOPIC_CHARS)):
        if value is None:
            continue
        problem = _field_problem(name, value, limit)
        if problem:
            raise _reject(request, problem, text, topic)

    # Needs at least one letter or digit once invisible characters are removed.
    # This rejects empty, whitespace-only, zero-width, emoji-only and punctuation-only text.
    if not any(c.isalnum() and c not in INVISIBLE_CHARS for c in text):
        raise _reject(request, "text has no readable content", text, topic)
    if topic is not None and topic.strip() and not any(c.isalnum() and c not in INVISIBLE_CHARS for c in topic):
        raise _reject(request, "topic has no readable content", text, topic)
    return TextRequest(text=text, topic=topic)


_served_first_request = False  # a fresh process (e.g. Render waking from idle) is a cold start


def client_ip(request: Request) -> str:
    # Behind Render's proxy the real client is the first X-Forwarded-For entry.
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    global _served_first_request
    if request.url.path not in AUDITED_PATHS:
        return await call_next(request)

    request_id = audit.new_request_id()
    cold_start = not _served_first_request
    _served_first_request = True
    request.state.request_id = request_id
    request.state.audit = {}  # the endpoint fills this in; we log it with the total latency
    start = time.perf_counter()

    common: dict[str, Any] = dict(
        request_id=request_id,
        endpoint=request.url.path,
        method=request.method,
        client_id=audit.hash_ip(client_ip(request)),  # raw IP is never logged or passed on
        cold_start=cold_start,
    )

    try:
        response = await asyncio.wait_for(call_next(request), timeout=REQUEST_TIMEOUT_S)
    except asyncio.TimeoutError:
        # The sync endpoint's worker thread can't be cancelled and finishes in the
        # background, but the caller gets a clear message instead of hanging.
        audit.log_failure(
            **common,
            latency_ms=(time.perf_counter() - start) * 1000,
            status_code=504,
            error_type="timeout",
            reason=f"exceeded {REQUEST_TIMEOUT_S:g}s limit",
            input_text=request.state.audit.get("input_text"),
            input_topic=request.state.audit.get("input_topic"),
        )
        response = JSONResponse(
            {"detail": f"Request timed out after {REQUEST_TIMEOUT_S:g}s, please retry"},
            status_code=504,
        )
    except Exception as exc:
        audit.log_failure(
            **common,
            latency_ms=(time.perf_counter() - start) * 1000,
            status_code=500,
            error_type="server_error",
            reason=f"{type(exc).__name__}: {exc}",
            input_text=request.state.audit.get("input_text"),
            input_topic=request.state.audit.get("input_topic"),
            stack_trace=traceback.format_exc(),
        )
        response = JSONResponse({"detail": "Internal server error"}, status_code=500)
    else:
        latency_ms = (time.perf_counter() - start) * 1000
        details = request.state.audit
        if response.status_code < 400 and "prediction" in details:
            audit.log_success(
                **common,
                latency_ms=latency_ms,
                status_code=response.status_code,
                input_text=details["input_text"],
                input_topic=details["input_topic"],
                **details["prediction"],
            )
        else:
            audit.log_failure(
                **common,
                latency_ms=latency_ms,
                status_code=response.status_code,
                error_type="validation" if response.status_code < 500 else "server_error",
                reason=details.get("reason", f"HTTP {response.status_code}"),
                input_text=details.get("input_text"),
                input_topic=details.get("input_topic"),
            )

    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    # Remaining FastAPI validation (e.g. a non-numeric X-Test-Delay header): 400, not 422.
    reason = "; ".join(f"{'.'.join(str(p) for p in e['loc'])}: {e['msg']}" for e in exc.errors())
    if hasattr(request.state, "audit"):
        request.state.audit["reason"] = reason
    return JSONResponse({"detail": reason}, status_code=400)


def valid_admin_token(token: Optional[str]) -> bool:
    expected = os.getenv("ADMIN_TOKEN")
    return bool(expected and token and hmac.compare_digest(token, expected))


@app.get("/logs")
def get_logs(x_admin_token: Optional[str] = Header(default=None), limit: Optional[int] = None):
    """Download the audit log as JSON lines. Disabled unless ADMIN_TOKEN is set on the server.
    The log holds user text, so it is token-protected. The file lives on Render's ephemeral
    disk and is lost on redeploy or spin-down: pull it soon after use (see pull_logs.py)."""
    if not os.getenv("ADMIN_TOKEN"):
        raise HTTPException(status_code=404, detail="Not Found")
    if not valid_admin_token(x_admin_token):
        raise HTTPException(status_code=401, detail="Invalid or missing X-Admin-Token")
    lines = [json.dumps(e, ensure_ascii=False) for e in audit.read_entries(limit)]
    return Response("\n".join(lines) + ("\n" if lines else ""), media_type="application/x-ndjson")


@app.get("/")
def health():
    return {"status": "ok"}


# no async def since session.run blocks, so FastAPI runs it in a threadpool.
@app.post("/predict")
def predict(
    request: Request,
    body: TextRequest = Depends(parse_body),
    x_test_delay: Optional[float] = Header(default=None),
    x_admin_token: Optional[str] = Header(default=None),
):
    topic = (body.topic or "").strip()
    audit_details = request.state.audit
    audit_details["input_text"] = body.text
    audit_details["input_topic"] = topic or None

    # Test hook for forcing timeouts: sleep before predicting. Ignored unless the
    # caller presents the admin token, so the public can't tie up the worker.
    if x_test_delay and valid_admin_token(x_admin_token):
        time.sleep(min(max(x_test_delay, 0.0), MAX_TEST_DELAY_S))

    t0 = time.perf_counter()
    if topic:
        # Topic post is context: encoded as the first segment of a text pair
        encoded = tokenizer.encode(topic, body.text)
    else:
        encoded = tokenizer.encode(body.text)

    inputs = {
        "input_ids": np.array([encoded.ids], dtype=np.int64),
        "attention_mask": np.array([encoded.attention_mask], dtype=np.int64),
    }
    if "token_type_ids" in INPUT_NAMES:
        inputs["token_type_ids"] = np.array([encoded.type_ids], dtype=np.int64)
    t1 = time.perf_counter()

    # shape (1, num_labels)
    logits = np.asarray(session.run(None, inputs)[0], dtype=np.float32)
    t2 = time.perf_counter()

    # Softmax to get probabilities
    exp_logits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
    probs = (exp_logits / np.sum(exp_logits, axis=-1, keepdims=True))[0]

    pred_id = int(np.argmax(probs))
    label = LABELS.get(pred_id, str(pred_id))
    scores = {LABELS.get(i, str(i)): round(float(p), 4) for i, p in enumerate(probs)}

    audit_details["prediction"] = {
        "chosen_label": label,
        "label_confidences": scores,
        "token_count": int(sum(encoded.attention_mask)),
        "truncated": len(encoded.overflowing) > 0,
        "preprocess_ms": (t1 - t0) * 1000,
        "inference_ms": (t2 - t1) * 1000,
    }
    return {
        "label": label,
        "confidence": round(float(probs[pred_id]), 4),
        "scores": scores,
        "used_topic": bool(topic),
        "request_id": request.state.request_id,
    }


# Deploy notes (Render free tier):
# - Commit render_model/model_quantized.onnx (~65MB), tokenizer.json and config.json
#   so Render bundles them into the container (GitHub limit is 100MB per file).
# - Start command: uvicorn app:app --host 0.0.0.0 --port $PORT --workers 1
#   One worker only: each worker duplicates the model in memory (512MB RAM limit).
# - Python version comes from .python-version; requirements.txt is runtime-only,
#   training libraries live in requirements-dev.txt.
