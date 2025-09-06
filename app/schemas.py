from pydantic import BaseModel
from typing import List, Any

class Detection(BaseModel):
    class_name: str
    confidence: float
    bbox: Any

class DetectionResponse(BaseModel):
    detections: List[Detection]
    result_image_url: str

class DetectionHistoryOut(BaseModel):
    id: int
    filename: str
    class_name: str
    confidence: float
    bbox: Any

    class Config:
        orm_mode = True
