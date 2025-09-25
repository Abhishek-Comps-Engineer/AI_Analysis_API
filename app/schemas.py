from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Any, Optional


class UserProfileOutSchema(BaseModel):
    profileImage_url: str
    email: EmailStr

class UserProfileSchema(UserProfileOutSchema):
    id :int
    
    class Config:
        from_attributes =True

class FloodEventSchema(BaseModel):
    id: int
    filename: str
    detected_at: datetime
    flood_percentage: float
    image_url: str

    class Config:
        from_attributes = True 

class LandAnalysisResponse(BaseModel):
    vegetation_cover: float
    water_cover: float
    soil_brightness: float
    ndvi_mean: float
    land_type: str
    land_use_case: str
    annotated_image: str   

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
        from_attributes = True


class BoundingBox(BaseModel):
    x_min: int
    y_min: int
    x_max: int
    y_max: int
    label: str
    confidence: float

class RoadAnalysisResponse(BaseModel):
    road_type: str
    road_condition: str
    road_lanes: Optional[int]
    damaged_areas: List[BoundingBox]
    processed_image_path: str


class RoadAnalysisHistoryOut(BaseModel):
    id: int
    filename: str
    road_type: str
    road_condition: str
    road_lanes: Optional[int]
    damaged_areas: List[BoundingBox]
    processed_image_path: str

    class Config:
        from_attributes = True

