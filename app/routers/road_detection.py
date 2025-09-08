import os
import shutil
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

from app.schemas import RoadAnalysisHistoryOut
from app.services.road_services import predict_image
from app.services.yolo_service import RESULTS_DIR
from app.utils import draw_bboxes
from ..models import RoadAnalysisHistory
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(prefix="/road", tags=["Road Analysis"])

@router.post("/analyze", response_model=RoadAnalysisHistoryOut)
async def analyze_road(file: UploadFile = File(...), db: Session = Depends(get_db)):

    file_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join("uploads", file_name)
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result, annotated_path = predict_image(file_path)

    damaged_areas = [
        {"x_min": 80, "y_min": 30, "x_max": 180, "y_max": 140, "label": "pothole", "confidence": 0.91}
    ]

    output_path = os.path.join("results", f"processed_{file_name}")
    os.makedirs("results", exist_ok=True)
    print(output_path)
    full_url = draw_bboxes(file_path, damaged_areas, output_path)

    db_entry = RoadAnalysisHistory(
        filename=file_name,
        road_type=result["road_type"],
        road_condition=result["road_condition"],
        road_lanes=2,
        damaged_areas=damaged_areas,
        processed_image_path=full_url  
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return db_entry

@router.get("/results/{id}")
def get_result_image(id: int, db: Session = Depends(get_db)):

    record = db.query(RoadAnalysisHistory).filter_by(id=id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    print(record)
    file_path = record.processed_image_path
    print(file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Processed image not found on disk")

    return FileResponse(file_path, media_type="image/jpeg")

@router.get("/history/", response_model=list[RoadAnalysisHistoryOut])
def get_history(db: Session = Depends(get_db)):
    records = db.query(RoadAnalysisHistory).all()
    return records
