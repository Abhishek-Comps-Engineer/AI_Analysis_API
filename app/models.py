from datetime import datetime
from sqlalchemy import JSON, Column, DateTime, Float, Integer, String 
from app.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer,primary_key=True,index=True)
    profileImage_url =  Column(String)
    email = Column(String,unique=True)



class FloodEvents(Base):
    __tablename__ = "FloodEvents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    detected_at = Column(DateTime, default=datetime.utcnow)
    flood_percentage = Column(Float)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ObjectDetectionHistory(Base):
    __tablename__ = "detection_history"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    class_name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    bbox = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class LandDetectionHistory(Base):
    __tablename__ = "land_detection_history"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    predicted_class = Column(String, index=True)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class LandType(Base):
    __tablename__ = "land_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  
    created_at = Column(DateTime, default=datetime.utcnow)
    
class UseCase(Base):
    __tablename__ = "use_cases"
    id = Column(Integer, primary_key=True, index=True)
    land_type_id = Column(Integer)  
    description = Column(String) 


class RoadAnalysisHistory(Base):
    __tablename__ = "road_analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    road_type = Column(String, nullable=False)
    road_condition = Column(String, nullable=False)
    road_lanes = Column(Integer)
    damaged_areas = Column(JSON)
    processed_image_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

