import torch
from torchvision import transforms
from PIL import Image, ImageDraw
import os
from models.potholmodel import RoadMultiTaskModel, road_types, road_conditions

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = RoadMultiTaskModel().to(device)
weights_path = os.path.join("app", "models", "road_multitask_model.pth")
if os.path.exists(weights_path):
    model.load_state_dict(torch.load(weights_path, map_location=device))
    model.eval()
    print("✅ Loaded trained weights")
else:
    print("⚠️ No trained weights found.")

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

def predict_image(img_path: str):
    model.eval()
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
    draw.text((10,10), f"Type: {result['road_type']}", fill=(255,0,0))
    draw.text((10,30), f"Condition: {result['road_condition']}", fill=(255,0,0))

    output_path = img_path.replace(".jpg","_out.jpg").replace(".png","_out.png")
    annotated.save(output_path)

    return result, output_path
