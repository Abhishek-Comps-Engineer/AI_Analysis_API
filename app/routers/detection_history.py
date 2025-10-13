from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import String, select, union_all, desc, literal
from app.database import get_db
from app.models import FloodEvents, ObjectDetectionHistory, LandDetectionHistory, RoadAnalysisHistory
from app.schemas import ActivityListResponse, ActivitySchema

router = APIRouter(
    prefix="/history",
    tags=["Detection History"]
)

@router.get("/",response_model=ActivityListResponse)
def get_recent_activity(db: Session = Depends(get_db), page: int = 1, limit: int = 20):
    
    stmt_flood = select(
        FloodEvents.id,
        FloodEvents.filename,
        FloodEvents.flood_percentage.cast(String).label("activity_detail"),
        FloodEvents.created_at,
        literal("Flood Map").label("activity_type")
    )

    stmt_object = select(
        ObjectDetectionHistory.id,
        ObjectDetectionHistory.filename,
        ObjectDetectionHistory.class_name.label("activity_detail"),
        ObjectDetectionHistory.created_at,
        literal("Object Detection").label("activity_type")
    )

    stmt_land = select(
        LandDetectionHistory.id,
        LandDetectionHistory.filename,
        LandDetectionHistory.predicted_class.label("activity_detail"),
        LandDetectionHistory.created_at,
        literal("Land Analysis").label("activity_type")
    )

    stmt_road = select(
        RoadAnalysisHistory.id,
        RoadAnalysisHistory.filename,
        RoadAnalysisHistory.road_condition.label("activity_detail"),
        RoadAnalysisHistory.created_at,
        literal("Road Analysis").label("activity_type")
    )

    combined = union_all(stmt_flood, stmt_object, stmt_land, stmt_road).order_by(desc("created_at"))

    results = db.execute(combined.offset((page-1)*limit).limit(limit)).fetchall()

    activities = [
        ActivitySchema(
            id=row.id,
            filename=row.filename,
            activity_detail=row.activity_detail,
            created_at=row.created_at,
            activity_type=row.activity_type
        )
        for row in results
    ]

    return {"activities":activities}
