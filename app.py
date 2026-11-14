import json
from pathlib import Path
from typing import Optional

import numpy as np
import onnxruntime as ort
from fastapi import FastAPI
from pydantic import BaseModel
from tokenizers import Tokenizer

MODEL_DIR = Path(__file__).parent / "render_model"

app = FastAPI()

# Load tokenizer and ONNX session once at startup
tokenizer = Tokenizer.from_file(str(MODEL_DIR / "tokenizer.json"))
tokenizer.enable_truncation(max_length=256)
tokenizer.enable_padding(pad_id=0, pad_token="[PAD]")

# Restrict threads to prevent memory spikes on Render's free tier
sess_options = ort.SessionOptions()
sess_options.intra_op_num_threads = 1
sess_options.inter_op_num_threads = 1

session = ort.InferenceSession(
    str(MODEL_DIR / "model_quantized.onnx"),
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


@app.get("/")
def health():
    return {"status": "ok"}


# no async def since session.run blocks, so FastAPI runs it in a threadpool.
@app.post("/predict")
def predict(request: TextRequest):
    topic = (request.topic or "").strip()
    if topic:
        # Topic post is context: encoded as the first segment of a text pair
        encoded = tokenizer.encode(topic, request.text)
    else:
        encoded = tokenizer.encode(request.text)

    inputs = {
        "input_ids": np.array([encoded.ids], dtype=np.int64),
        "attention_mask": np.array([encoded.attention_mask], dtype=np.int64),
    }
    if "token_type_ids" in INPUT_NAMES:
        inputs["token_type_ids"] = np.array([encoded.type_ids], dtype=np.int64)

    # shape (1, num_labels)
    logits = np.asarray(session.run(None, inputs)[0], dtype=np.float32)

    # Softmax to get probabilities
    exp_logits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
    probs = (exp_logits / np.sum(exp_logits, axis=-1, keepdims=True))[0]

    pred_id = int(np.argmax(probs))
    return {
        "label": LABELS.get(pred_id, str(pred_id)),
        "confidence": round(float(probs[pred_id]), 4),
        "scores": {LABELS.get(i, str(i)): round(float(p), 4) for i, p in enumerate(probs)},
        "used_topic": bool(topic),
    }


# Deploy notes (Render free tier):
# - Commit render_model/model_quantized.onnx (~65MB), tokenizer.json and config.json
#   so Render bundles them into the container (GitHub limit is 100MB per file).
# - Start command: uvicorn app:app --host 0.0.0.0 --port $PORT --workers 1
#   One worker only: each worker duplicates the model in memory (512MB RAM limit).
# - Python version comes from .python-version; requirements.txt is runtime-only,
#   training libraries live in requirements-dev.txt.
