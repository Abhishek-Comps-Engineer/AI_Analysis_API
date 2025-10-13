import torch
from torchvision import transforms
from PIL import Image, ImageDraw
import os
from models.potholmodel import RoadMultiTaskModel, road_types, road_conditions

device = torch.device("cpu")

model = RoadMultiTaskModel().to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

def predict_image(img_path: str, results_dir: str):

    img = Image.open(img_path).convert("RGB")
    t_img = transform(img).unsqueeze(0).to(device)  

    with torch.no_grad():
        type_out, cond_out = model(t_img)
        type_pred = torch.argmax(type_out, dim=1).item()
        cond_pred = torch.argmax(cond_out, dim=1).item()

    result = {
        "road_type": road_types[type_pred],
        "road_condition": road_conditions[cond_pred]
    }

    annotated = img.copy()
    draw = ImageDraw.Draw(annotated)
    draw.text((10, 10), f"Type: {result['road_type']}", fill=(255, 0, 0))
    draw.text((10, 30), f"Condition: {result['road_condition']}", fill=(255, 0, 0))

    os.makedirs(results_dir, exist_ok=True)
    base_name = os.path.basename(img_path)
    output_path = os.path.join(results_dir, f"processed_{base_name}")
    annotated.save(output_path, format="JPEG")

    return result, output_path
