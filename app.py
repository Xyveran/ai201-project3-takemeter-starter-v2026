import hmac
import json
import os
import time
import traceback
from pathlib import Path
from typing import Any, Optional

import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from tokenizers import Tokenizer

import audit

MODEL_DIR = Path(__file__).parent / "render_model"
MODEL_PATH = MODEL_DIR / "model_quantized.onnx"
AUDITED_PATHS = {"/predict"}  # health checks on "/" are not logged

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


class TextRequest(BaseModel):
    text: str
    topic: Optional[str] = None  # optional context; ignored when absent or blank


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
        response = await call_next(request)
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
    # Malformed body (missing/non-string text, bad JSON): record why, then return FastAPI's default 422.
    errors = exc.errors()
    if hasattr(request.state, "audit"):
        request.state.audit["reason"] = "; ".join(
            f"{'.'.join(str(p) for p in e['loc'])}: {e['msg']}" for e in errors
        )
    return await request_validation_exception_handler(request, exc)


@app.get("/logs")
def get_logs(x_admin_token: Optional[str] = Header(default=None), limit: Optional[int] = None):
    """Download the audit log as JSON lines. Disabled unless ADMIN_TOKEN is set on the server.
    The log holds user text, so it is token-protected. The file lives on Render's ephemeral
    disk and is lost on redeploy or spin-down: pull it soon after use (see pull_logs.py)."""
    expected = os.getenv("ADMIN_TOKEN")
    if not expected:
        raise HTTPException(status_code=404, detail="Not Found")
    if not x_admin_token or not hmac.compare_digest(x_admin_token, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing X-Admin-Token")
    lines = [json.dumps(e, ensure_ascii=False) for e in audit.read_entries(limit)]
    return Response("\n".join(lines) + ("\n" if lines else ""), media_type="application/x-ndjson")


@app.get("/")
def health():
    return {"status": "ok"}


# no async def since session.run blocks, so FastAPI runs it in a threadpool.
@app.post("/predict")
def predict(request: Request, body: TextRequest):
    topic = (body.topic or "").strip()
    audit_details = request.state.audit
    audit_details["input_text"] = body.text
    audit_details["input_topic"] = topic or None

    if not body.text.strip():
        audit_details["reason"] = "empty text"
        raise HTTPException(status_code=400, detail="text must not be empty")

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
