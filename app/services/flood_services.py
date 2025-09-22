import os
from datetime import datetime
import numpy as np
from PIL import Image
from io import BytesIO
from models import flood_model as fd
from app.services.object_service import UPLOAD_DIR



def run_flood_analysis(image_bytes: bytes, filename: str):
    """Run flood detection and save result image"""
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    inputs = fd.preprocess_image(image)
    if fd.torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    with fd.torch.no_grad():
        outputs = fd.model(**inputs)

    mask = fd.postprocess_mask(outputs.logits)
    orig_np = np.array(image)
    result_np = fd.overlay_mask(orig_np, mask)

    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_path = os.path.join(UPLOAD_DIR, f"result_{timestamp}_{filename}.png")
    Image.fromarray(result_np).save(result_path)

    return result_path
