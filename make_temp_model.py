# Builds a tiny stand-in model in ./render_model so the Render service can be
# deployed and tested before the real fine-tuned model is exported.
# Same interface as the real one: input_ids + attention_mask -> logits (1, 3).
# Predictions are meaningless. Re-running run_onnx_export.py overwrites these files.
import json
from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.processors import TemplateProcessing

out = Path(__file__).parent / "render_model"
out.mkdir(exist_ok=True)

# Tokenizer: [PAD]=0 like DistilBERT; unknown words map to [UNK]
vocab = {"[PAD]": 0, "[UNK]": 1, "[CLS]": 2, "[SEP]": 3}
tok = Tokenizer(WordLevel(vocab, unk_token="[UNK]"))
tok.pre_tokenizer = Whitespace()
tok.post_processor = TemplateProcessing(
    single="[CLS] $A [SEP]",
    pair="[CLS] $A [SEP] $B:1 [SEP]:1",
    special_tokens=[("[CLS]", 2), ("[SEP]", 3)],
)
tok.save(str(out / "tokenizer.json"))

# Model: logits = sum over unmasked tokens of a fixed embedding row (vocab 4 -> 3 classes)
rng = np.random.default_rng(0)
emb = helper.make_tensor("emb", TensorProto.FLOAT, [4, 3], rng.normal(size=12).astype(np.float32))
ids = helper.make_tensor_value_info("input_ids", TensorProto.INT64, [1, "seq"])
mask = helper.make_tensor_value_info("attention_mask", TensorProto.INT64, [1, "seq"])
logits = helper.make_tensor_value_info("logits", TensorProto.FLOAT, [1, 3])
axes = helper.make_tensor("axes", TensorProto.INT64, [1], [1])
nodes = [
    helper.make_node("Gather", ["emb", "input_ids"], ["g"]),  # (1, seq, 3)
    helper.make_node("Cast", ["attention_mask"], ["m"], to=TensorProto.FLOAT),  # (1, seq)
    helper.make_node("Unsqueeze", ["m", "axes_u"], ["m3"]),  # (1, seq, 1)
    helper.make_node("Mul", ["g", "m3"], ["gm"]),
    helper.make_node("ReduceSum", ["gm", "axes"], ["logits"], keepdims=0),  # (1, 3)
]
axes_u = helper.make_tensor("axes_u", TensorProto.INT64, [1], [2])
graph = helper.make_graph(nodes, "temp", [ids, mask], [logits], initializer=[emb, axes, axes_u])
model = helper.make_model(graph, opset_imports=[helper.make_opsetid("", 17)])
model.ir_version = 9
onnx.checker.check_model(model)
onnx.save(model, str(out / "model_quantized.onnx"))

# Same label order as the notebook's LABELS
labels = ["fluff", "substantive", "derailing"]
(out / "config.json").write_text(
    json.dumps({"id2label": dict(enumerate(labels)), "label2id": {l: i for i, l in enumerate(labels)}}, indent=2)
)
print("Temp model written to", out)
