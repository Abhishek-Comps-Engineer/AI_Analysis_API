from ultralytics import YOLO


model = YOLO(r"models\yolov8l.pt")


def run_yolo(file_path: str, save_path: str):
    results = model(file_path)
    result = results[0]
    result.save(filename=save_path)
    return result
