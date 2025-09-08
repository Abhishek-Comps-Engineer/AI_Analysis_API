import torch
import torch.nn.functional as F
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import io
from sqlalchemy.orm import Session
from app.models import LandType, UseCase


MODEL_NAME = "prithivMLmods/GiD-Land-Cover-Classification"
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)

def predict_land_cover(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    probs = F.softmax(logits, dim=-1)[0]
    
    predicted_class_idx = logits.argmax(-1).item()
    predicted_label = model.config.id2label[predicted_class_idx]
    confidence = float(probs[predicted_class_idx])
    
    return predicted_label, confidence

def get_use_cases(db: Session, land_name: str):
    land = db.query(LandType).filter(LandType.name==land_name).first()
    if not land:
        return ["No suggestions available for this land type."]
    use_cases = db.query(UseCase).filter(UseCase.land_type_id==land.id).all()
    return [uc.description for uc in use_cases]
