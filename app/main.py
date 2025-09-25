import os
from fastapi import FastAPI
from app.routers import  flood_detection, land_detection, object_detection, road_detection, user_profile
from app.services.object_service import RESULTS_DIR
from .database import engine
from fastapi.middleware.cors import CORSMiddleware   
from app import models
from fastapi.staticfiles import StaticFiles


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
   title="AI ANALYSIS API",
)

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


app.include_router(user_profile.router)
app.include_router(flood_detection.router)
app.include_router(object_detection.router)
app.include_router(road_detection.router)
app.include_router(land_detection.router)


app.mount("/results", StaticFiles(directory=RESULTS_DIR), name="static_results")
app.mount("/profiles", StaticFiles(directory=user_profile.PROFILES_DIR), name="static_results")


@app.get("/")
def getStart():
    return {"message": "Welcome!, Visit http://127.0.0.1:8000/docs to access the full API features."}
