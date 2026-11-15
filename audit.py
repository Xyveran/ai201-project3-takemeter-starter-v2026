import hashlib
import json
import os
import sys
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

PATH = Path(__file__).parent
LOG_DIR = PATH / "logs"
USAGE_LOG = LOG_DIR / "use.jsonl"

# LOG_INPUT_TEXT=0 keeps raw post text out of the logs (hash + length are still logged).
LOG_INPUT_TEXT = os.getenv("LOG_INPUT_TEXT", "1") != "0"
# LOG_STDOUT=0 stops echoing each entry to stdout (Render's log viewer reads stdout).
LOG_STDOUT = os.getenv("LOG_STDOUT", "1") != "0"
# Predictions whose top confidence is below this are flagged for review.
LOW_CONFIDENCE_THRESHOLD = float(os.getenv("LOW_CONFIDENCE_THRESHOLD", "0.6"))

# Deploy identity. Render sets RENDER_GIT_COMMIT and RENDER_INSTANCE_ID automatically.
APP_VERSION = os.getenv("APP_VERSION") or os.getenv("RENDER_GIT_COMMIT")
INSTANCE_ID = os.getenv("RENDER_INSTANCE_ID") or os.getenv("RENDER_SERVICE_ID")

_model_info: dict[str, str | bool | None] = {
    "model_name": None,
    "model_version": None,
    "model_quantized": None,
}
_lock = threading.Lock()


def configure_model(name: str, version: str, quantized: bool) -> None:
    """Call once at startup so every entry records which model produced it."""
    _model_info.update(model_name=name, model_version=version, model_quantized=quantized)


def file_fingerprint(path: Path, length: int = 12) -> str:
    """Short SHA-256 of a file, used as a model version that changes whenever the weights do."""
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:length]


def new_request_id() -> str:
    return uuid.uuid4().hex


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_ip(ip: str) -> str:
    return _sha256(ip)[:16]


def _append(entry: dict) -> dict:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False)
    with _lock:
        with USAGE_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    if LOG_STDOUT:
        print(line, file=sys.stdout, flush=True)
    return entry


def _base(
    *,
    event: str,
    request_id: str,
    endpoint: str,
    method: str,
    client_id: str,
    status_code: int,
    latency_ms: float,
    cold_start: bool,
    input_text: str | None,
    input_topic: str | None,
) -> dict:
    return {
        "timestamp": _now(),
        "event": event,
        "request_id": request_id,
        "endpoint": endpoint,
        "method": method,
        "client_id": client_id,
        "status_code": status_code,
        "latency_ms": round(latency_ms, 2),
        "cold_start": cold_start,
        # input (text may be absent when the request failed validation)
        "input_text": input_text if LOG_INPUT_TEXT else None,
        "text_hash": _sha256(input_text) if input_text is not None else None,
        "text_length": len(input_text) if input_text is not None else None,
        "input_topic": input_topic,
        "topic_provided": bool(input_topic and input_topic.strip()),
        # model / deploy
        **_model_info,
        "app_version": APP_VERSION,
        "instance_id": INSTANCE_ID,
    }


def log_success(
    *,
    request_id: str,
    endpoint: str,
    method: str,
    client_id: str,
    latency_ms: float,
    cold_start: bool,
    input_text: str,
    input_topic: str | None,
    chosen_label: str,
    label_confidences: dict[str, float],
    token_count: int,
    truncated: bool,
    preprocess_ms: float,
    inference_ms: float,
    status_code: int = 200,
) -> dict:
    scores = sorted(label_confidences.values(), reverse=True)
    top = scores[0]
    entry = _base(
        event="prediction",
        request_id=request_id,
        endpoint=endpoint,
        method=method,
        client_id=client_id,
        status_code=status_code,
        latency_ms=latency_ms,
        cold_start=cold_start,
        input_text=input_text,
        input_topic=input_topic,
    )
    entry.update({
        "chosen_label": chosen_label,
        "confidence": top,
        "margin": round(top - scores[1], 4) if len(scores) > 1 else None,  # small = borderline
        "low_confidence": top < LOW_CONFIDENCE_THRESHOLD,
        "label_confidences": label_confidences,
        "token_count": token_count,
        "truncated": truncated,
        "preprocess_ms": round(preprocess_ms, 2),
        "inference_ms": round(inference_ms, 2),
        # feedback loop: filled in later via record_feedback(), joined on request_id
        "corrected_label": None,
        "feedback": None,
    })
    return _append(entry)


def log_failure(
    *,
    request_id: str,
    endpoint: str,
    method: str,
    client_id: str,
    latency_ms: float,
    cold_start: bool,
    status_code: int,
    error_type: str,  # "validation" for bad input, "server_error" for a crash
    reason: str,
    input_text: str | None = None,
    input_topic: str | None = None,
    stack_trace: str | None = None,  # only for server errors, not validation failures
) -> dict:
    entry = _base(
        event="rejected",
        request_id=request_id,
        endpoint=endpoint,
        method=method,
        client_id=client_id,
        status_code=status_code,
        latency_ms=latency_ms,
        cold_start=cold_start,
        input_text=input_text,
        input_topic=input_topic,
    )
    entry.update({
        "error_type": error_type,
        "reason": reason,
        "stack_trace": stack_trace,
    })
    return _append(entry)


def record_feedback(request_id: str, corrected_label: str | None = None, feedback: str | None = None) -> dict:
    """Append a feedback event that joins back to a prediction on request_id."""
    return _append({
        "timestamp": _now(),
        "event": "feedback",
        "request_id": request_id,
        "corrected_label": corrected_label,
        "feedback": feedback,
    })


def read_entries(limit: int | None = None) -> list[dict]:
    if not USAGE_LOG.exists():
        return []

    entries = []
    for line in USAGE_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    return entries[-limit:] if limit else entries


def entries_for(client_id: str) -> list[dict]:
    return [e for e in read_entries() if e.get("client_id") == client_id]


def entries_for_request(request_id: str) -> list[dict]:
    return [e for e in read_entries() if e.get("request_id") == request_id]


def clear() -> int:
    count = len(read_entries())
    if USAGE_LOG.exists():
        USAGE_LOG.unlink()
    return count
