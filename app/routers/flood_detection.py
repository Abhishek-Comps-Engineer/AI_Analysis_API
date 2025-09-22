import os
import uuid
from PIL import Image, ImageDraw, ImageFont
from fastapi import APIRouter, FastAPI, File, HTTPException, UploadFile, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from app.models import FloodHistory, LandDetectionHistory
from app.services.flood_services import run_flood_analysis
from app.services.land_services import get_use_cases, predict_land_cover
from app.database import get_db, Base, engine
from app.routers.land_detection import predict_land_cover
import shutil


from app.services.object_service import RESULTS_DIR, UPLOAD_DIR

router = APIRouter(prefix="/flood", tags=["Flood Analysis"])


@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...), db=Depends(get_db)):
    if file.content_type.split('/')[0] != 'image':
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()
    result_path = run_flood_analysis(contents, file.filename)

    # Save record in DB
    record = FloodHistory(
        filename=file.filename,
        status="completed",
        result_path=result_path
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {"id": record.id, "result_path": record.result_path}

@router.get("/{analysis_id}")
def get_history(analysis_id: int, db=Depends(get_db)):
    record = db.query(FloodHistory).filter(FloodHistory.id == analysis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return {
        "id": record.id,
        "filename": record.filename,
        "created_at": record.created_at,
        "status": record.status,
        "result_path": record.result_path
    }

@router.get("/{analysis_id}")
def download_result(analysis_id: int, db=Depends(get_db)):
    record = db.query(FloodHistory).filter(FloodHistory.id == analysis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    if not os.path.exists(record.result_path):
        raise HTTPException(status_code=404, detail="Result image missing")

    return FileResponse(record.result_path)



