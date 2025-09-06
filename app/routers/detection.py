from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from fastapi.responses import Response
import uuid, os

from ..database import SessionLocal, get_db
from ..models import DetectionHistory
from ..schemas import DetectionResponse, DetectionHistoryOut
from ..services.yolo_service import run_yolo, UPLOAD_DIR, RESULTS_DIR

router = APIRouter(prefix="/detect", tags=["Detection"])

@router.post("/", response_model=DetectionResponse)
async def detect_objects(file: UploadFile = File(...)):
    db: Session = SessionLocal()

    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as f:
        f.write(await file.read())

   
    result_img_path = os.path.join(RESULTS_DIR, file_name)
    result = run_yolo(file_path, result_img_path)

  
    detections = []
    for box in result.boxes:
        detection = {
            "class_name": result.names[int(box.cls)],
            "confidence": float(box.conf),
            "bbox": box.xyxy.tolist()
        }
        detections.append(detection)

       
        db_entry = DetectionHistory(
            filename=file_name,
            class_name=detection["class_name"],
            confidence=detection["confidence"],
            bbox=detection["bbox"]
        )
        db.add(db_entry)

    db.commit()
    db.close()
    return {"detections": detections, "result_image_url": f"/results/{file_name}"}


# RESULTS_DIR = "/absolute/path/to/results" 


@router.get("/results/{id}")
def get_result_image(id: int, db: Session = Depends(get_db)):
    record = db.query(DetectionHistory).filter_by(id=id).first()

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
    records = db.query(DetectionHistory).all()
    db.close()
    return records
