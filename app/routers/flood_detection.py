import os
import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FloodEvents
from app.schemas import FloodEventSchema
from app.services.flood_services import detect_flood
from app.services.object_service import RESULTS_DIR
router = APIRouter(prefix="/flood", tags=["Flood Detection"])

@router.post("/", response_model=FloodEventSchema)
async def detect_flood_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db)):
   
    try:        
        image_data = await file.read()
        blended_image_bytes, flood_percentage = detect_flood(image_data)
        
        unique_filename = f"flood_{uuid.uuid4()}.png"
        file_path = os.path.join(RESULTS_DIR, unique_filename) # Correct way to join paths
        with open(file_path, "wb") as f:
            f.write(blended_image_bytes)
            
        db_flood_event = FloodEvents(
            filename=unique_filename,
            flood_percentage=float(flood_percentage),
            detected_at=datetime.utcnow(),
            image_url=f"/{RESULTS_DIR}/{unique_filename}"
        )
        db.add(db_flood_event)
        db.commit()
        db.refresh(db_flood_event)

        return db_flood_event

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=list[FloodEventSchema])
def get_flood_history(db: Session = Depends(get_db)):
 
    events = db.query(FloodEvents).all()
    return events