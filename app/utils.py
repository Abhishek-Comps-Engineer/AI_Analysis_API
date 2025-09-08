import os
import cv2



def draw_bboxes(image_path: str, predictions: list, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = cv2.imread(image_path)

    for pred in predictions:
        x_min, y_min, x_max, y_max = pred["x_min"], pred["y_min"], pred["x_max"], pred["y_max"]
        label, conf = pred["label"], pred["confidence"]
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0,255,0), 2)
        cv2.putText(img, f"{label} {conf:.2f}", (x_min, y_min-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    cv2.imwrite(output_path, img)

    return os.path.relpath(output_path)


