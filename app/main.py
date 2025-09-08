import os
from fastapi import FastAPI
from app.routers import  land_detection, object_detection, road_detection
from app.services.yolo_service import RESULTS_DIR
from .database import engine
from app import models
from fastapi.staticfiles import StaticFiles


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
   title="AI ANALYSIS API",
)

app.include_router(object_detection.router)
app.include_router(road_detection.router)
# app.include_router(crop_detection.router)
app.include_router(land_detection.router)

app.mount("/results", StaticFiles(directory=RESULTS_DIR), name="static_results")


