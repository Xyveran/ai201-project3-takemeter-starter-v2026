# Export and Quantize Locally

from optimum.onnxruntime import ORTModelForSequenceClassification, ORTQuantizer
from optimum.onnxruntime.configuration import AutoQuantizationConfig
from transformers import AutoTokenizer

# Path to fine-tuned PyTorch model dir
model_path = "./my-finetuned-distilbert"
onnx_path = "./onnx-temp"
quantized_path = "./render_model"

# Export PyTorch model to ONNX
model = ORTModelForSequenceClassification.from_pretrained(model_path, export=True)
tokenizer = AutoTokenizer.from_pretrained(model_path)

model.save_pretrained(onnx_path)
tokenizer.save_pretrained(quantized_path)

# Quantize to INT8 (cuts size from 256MB to 64MB) and save to Render's model dir
quantizer = ORTQuantizer.from_pretrained(onnx_path)
qconfig = AutoQuantizationConfig.avx2(is_static=False, per_channel=False)
quantizer.quantize(save_dir=quantized_path, quantization_config=qconfig)

# Check ./render_model folder to confirm that model_quantized.onnx is around 65MB and tokenizer.json is present.