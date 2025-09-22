import numpy as np
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForSemanticSegmentation
from huggingface_hub import snapshot_download

model_path = snapshot_download(r"ibm-nasa-geospatial/Prithvi-EO-1.0-100M-sen1floods11")
print("Model downloaded to:", model_path)

model_name = r"ibm-nasa-geospatial/Prithvi-EO-1.0-100M-sen1floods11"

processor = AutoProcessor.from_pretrained(model_name,trust_remote_code=True)
model = AutoModelForSemanticSegmentation.from_pretrained(model_name)

model.eval()
if torch.cuda.is_available():
    model = model.to("cuda")
print("Abhshek Sharma")
print("Feature extractor path:", processor.cache_dir)
print("Model path:", model.config._name_or_path)

def preprocess_image(image: Image.Image):
    """Convert PIL to tensor for model input"""
    inputs = processor(images=image, return_tensors="pt")
    return inputs

def postprocess_mask(mask_logits, threshold=0.5):
    """Convert logits to binary flood mask"""
    probs = torch.softmax(mask_logits, dim=1)
    water_prob = probs[:, 1, :, :]   # class 1 = flood/water
    mask = (water_prob > threshold).cpu().numpy().astype(np.uint8) * 255
    return mask[0]  # remove batch

def overlay_mask(orig_np: np.ndarray, mask_np: np.ndarray, color=(255, 0, 0), alpha=0.4):
    """Overlay flood mask on image"""
    mask_bool = mask_np > 127
    overlay = np.zeros_like(orig_np, dtype=np.uint8)
    overlay[:] = color
    blended = np.where(
        mask_bool[..., None],
        (orig_np * (1 - alpha) + overlay * alpha).astype(np.uint8),
        orig_np
    )
    return blended
