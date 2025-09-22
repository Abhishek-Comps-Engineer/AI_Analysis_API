import os
import uuid
from PIL import Image, ImageDraw, ImageFont
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from app.models import LandDetectionHistory
from app.services.land_services import get_use_cases, predict_land_cover
from app.database import get_db
from app.routers.land_detection import predict_land_cover

from app.services.object_service import RESULTS_DIR, UPLOAD_DIR


router = APIRouter(prefix="/land", tags=["Land Analysis"])


@router.post("/")
async def detect_land(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    upload_path = os.path.join(UPLOAD_DIR, file_name)

    with open(upload_path, "wb") as f:
        f.write(await file.read())

    predicted_label, confidence = predict_land_cover(open(upload_path, "rb").read())

    suggestions = get_use_cases(db, predicted_label)

    image = Image.open(upload_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=18.0)
    draw.text((10, 10), f"{predicted_label} ({confidence:.2f})", fill="red", font=font)

    result_file_path = os.path.join(RESULTS_DIR, file_name)
    image.save(result_file_path)

    db_entry = LandDetectionHistory(
        filename=file_name,
        predicted_class=predicted_label,
        confidence=confidence
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return {
        "id": db_entry.id,
        "predicted_class": predicted_label,
        "confidence": confidence,
        "suggested_use_cases": suggestions,
        "annotated_image_url": result_file_path
    }


@router.get("/results/{id}")
def get_result_image(id: int, db: Session = Depends(get_db)):
    record = db.query(LandDetectionHistory).filter_by(id=id).first()
    if not record:
        return JSONResponse(content={"error": "Not found"}, status_code=404)

    file_path = os.path.join(RESULTS_DIR, record.filename)
    if not os.path.exists(file_path):
        return JSONResponse(content={"error": "File not found"}, status_code=404)

    return FileResponse(file_path, media_type="image/png")


@router.get("/history/")
def get_history(db: Session = Depends(get_db)):
    records = db.query(LandDetectionHistory).all()
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "predicted_class": r.predicted_class,
            "confidence": r.confidence
        } for r in records
    ]
