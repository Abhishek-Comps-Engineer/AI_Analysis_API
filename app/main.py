import os
import uvicorn
from fastapi import FastAPI
from app.routers import detection_history, flood_detection, land_detection, object_detection, road_detection, user_profile
from app.utils import RESULTS_DIR
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from app import models
from fastapi.staticfiles import StaticFiles

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI ANALYSIS API")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8000",
    "http://10.0.2.2:8000",
    "http://192.168.1.*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(user_profile.router)
app.include_router(flood_detection.router)
app.include_router(object_detection.router)
app.include_router(road_detection.router)
app.include_router(land_detection.router)
app.include_router(detection_history.router)

# Static directories
app.mount("/results", StaticFiles(directory=RESULTS_DIR), name="static_results")
app.mount("/profiles", StaticFiles(directory=user_profile.PROFILES_DIR), name="static_profiles")

@app.get("/")
def get_start():
    return {"message": "Welcome! Visit /docs to access the API documentation."}

if __name__ == "__main__":
    os.environ["PORT"] = os.environ.get("PORT", "10000")
    port = int(os.environ["PORT"])
    print(f"Starting server on port {port}...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
