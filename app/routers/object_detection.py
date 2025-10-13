from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
import uuid, os

from app.utils import RESULTS_DIR, UPLOADS_DIR
from ..database import SessionLocal, get_db
from ..models import ObjectDetectionHistory
from ..schemas import DetectionResponse, DetectionHistoryOut
from ..services.object_service import run_yolo

router = APIRouter(prefix="/detect", tags=["Object Detection"])

@router.post("/", response_model=DetectionResponse)
async def detect_objects(file: UploadFile = File(...),db: Session = Depends(get_db)):
    
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOADS_DIR, file_name)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    result_img_path = os.path.join(RESULTS_DIR, file_name)
    result = run_yolo(file_path, result_img_path)

    file_path = ""
  
    detections = []
    for box in result.boxes:
        detection = {
            "class_name": result.names[int(box.cls)],
            "confidence": float(box.conf),
            "bbox": box.xyxy.tolist()
        }
        detections.append(detection)

       
        db_entry = ObjectDetectionHistory(
            filename=file_name,
            class_name=detection["class_name"],
            confidence=detection["confidence"],
            bbox=detection["bbox"]
        )
        db.add(db_entry)
        file_path = os.path.join(RESULTS_DIR, file_name)

    db.commit()
    db.close()  
    return {"detections": detections, "result_image_url": file_path}


@router.get("/results/{id}")
def get_result_image(id: int, db: Session = Depends(get_db)):
    record = db.query(ObjectDetectionHistory).filter_by(id=id).first()

    print(record)
    if not record:
        return JSONResponse(content={"error": "Not found"}, status_code=404)
    
    file_path = os.path.join(RESULTS_DIR, record.filename)

    if not os.path.exists(file_path):
        return JSONResponse(content={"error": "File not found"}, status_code=404)

    return FileResponse(file_path, media_type="image/jpeg")


@router.get("/history/", response_model=list[DetectionHistoryOut])
def get_history():
    db: Session = SessionLocal()
    records = db.query(ObjectDetectionHistory).all()
    db.close()
    return records
