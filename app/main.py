from fastapi import FastAPI
from app.routers import detection
from .database import engine, test_connection
from app import models
from fastapi.staticfiles import StaticFiles


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
   title="AI ANALYSIS API",
)


app.include_router(detection.router)

app.mount("/detect/results", StaticFiles(directory="results"), name="results")

@app.get("/")
def get():
   test_connection()
   return {"data":"My Message"}
