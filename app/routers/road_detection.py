import os
import shutil
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

from app.schemas import RoadAnalysisHistoryOut
from app.services.road_services import predict_image
from app.utils import RESULTS_DIR, UPLOADS_DIR
from ..models import RoadAnalysisHistory
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(prefix="/road", tags=["Road Analysis"])

@router.post("/analyze", response_model=RoadAnalysisHistoryOut)
async def analyze_road(file: UploadFile = File(...), db: Session = Depends(get_db)):

    file_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOADS_DIR, file_name)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result,output_path = predict_image(file_path,RESULTS_DIR)
   
    print("UPLOADS_DIR:", UPLOADS_DIR)
    print("RESULTS_DIR:", RESULTS_DIR)
    print("Processed image path:", output_path)

    db_entry = RoadAnalysisHistory(
        filename=file_name,
        road_type=result["road_type"],
        road_condition=result["road_condition"],
        road_lanes=2,
        processed_image_path=output_path  
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
        raise HTTPException(status_code=404,
                             detail="Processed image not found on disk")

    return FileResponse(file_path, media_type="image/jpeg")

@router.get("/history/", response_model=list[RoadAnalysisHistoryOut])
def get_history(db: Session = Depends(get_db)):
    records = db.query(RoadAnalysisHistory).all()
    return records
