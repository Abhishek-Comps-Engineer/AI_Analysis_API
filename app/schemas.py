from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Any, Optional

class ActivitySchema(BaseModel):
    id: int
    filename: str
    activity_detail: str
    created_at: datetime
    activity_type: str

    class Config:
        from_attributes = True

class ActivityListResponse(BaseModel):
    activities: List[ActivitySchema]


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
    processed_image_path: str


class RoadAnalysisHistoryOut(BaseModel):
    id: int
    filename: str
    road_type: str
    road_condition: str
    road_lanes: Optional[int]
    processed_image_path: str

    class Config:
        from_attributes = True

