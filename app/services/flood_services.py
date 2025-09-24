import torch
import cv2
import numpy as np
import io
from PIL import Image
import segmentation_models_pytorch as smp

model = smp.Unet(
    encoder_name="mobilenet_v2",
    encoder_weights=None,
    in_channels=3,
    classes=1,
    activation='sigmoid'
)
model.load_state_dict(torch.load(r"models\flood_detection_model.pth"))
model.eval()

def detect_flood(image_data: bytes):
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    image_np = np.array(image)
    original_size = image_np.shape[:2]
    resize_to = (256, 256)
    image_resized = cv2.resize(image_np, resize_to)
    image_tensor = image_resized.astype(np.float32) / 255.0
    image_tensor = torch.from_numpy(image_tensor).permute(2, 0, 1).unsqueeze(0)
    
    with torch.no_grad():
        prediction = model(image_tensor)
        predicted_mask = (prediction.squeeze().cpu().numpy() > 0.5).astype(np.uint8)

    flood_pixels = np.sum(predicted_mask)
    total_pixels = predicted_mask.size
    flood_percentage = (flood_pixels / total_pixels) * 100
    
    predicted_mask_resized = cv2.resize(predicted_mask, (original_size[1], original_size[0]), interpolation=cv2.INTER_NEAREST)
    flood_overlay = np.zeros_like(image_np)
    flood_overlay[predicted_mask_resized == 1] = [0, 100, 255] # Blue-ish color
    alpha = 0.5
    blended_image = image_np * (1 - alpha) + flood_overlay * alpha
    blended_image = blended_image.astype(np.uint8)
    
    blended_pil = Image.fromarray(blended_image)
    output_buffer = io.BytesIO()
    blended_pil.save(output_buffer, format="PNG")
    
    return output_buffer.getvalue(), flood_percentage