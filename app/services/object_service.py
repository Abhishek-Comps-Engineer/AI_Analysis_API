from ultralytics import YOLO
import os

model = YOLO(r"models\yolov8n.pt")

UPLOAD_DIR = "uploads"
RESULTS_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


def run_yolo(file_path: str, save_path: str):
    results = model(file_path)
    result = results[0]
    result.save(filename=save_path)
    return result
