import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from PIL import Image
from torchvision.models import resnet18, ResNet18_Weights

import torch
print("CUDA Available:", torch.cuda.is_available())
print("Device Name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU only")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# Dataset root (all classes inside this folder)
data_dir = r"C:\Users\Abhi\Downloads\Plant_leaf_diseases_dataset_with_augmentation\PlantVillage"

# -----------------------------
# 1. Transforms
# -----------------------------
train_transforms = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(20),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

# -----------------------------
# 2. Load dataset using ImageFolder
# -----------------------------
full_dataset = datasets.ImageFolder(root=data_dir, transform=train_transforms)
class_names = full_dataset.classes
print("Classes:", class_names)

# -----------------------------
# 3. Split into train/val (80/20)
# -----------------------------
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

# Apply validation transforms to val_dataset
val_dataset.dataset.transform = val_transforms

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_dataset, batch_size=32, shuffle=False)

# -----------------------------
# 4. Define model (ResNet18)
# -----------------------------
weights = ResNet18_Weights.DEFAULT  # most up-to-date pretrained weights
model = resnet18(weights=weights)
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, len(class_names))
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# -----------------------------
# 5. Training loop
# -----------------------------
def train_model(model, criterion, optimizer, train_loader, val_loader, epochs=5):
    for epoch in range(epochs):
        model.train()
        running_loss, running_corrects = 0.0, 0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs, 1)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = running_corrects.double() / len(train_loader.dataset)

        # Validation
        model.eval()
        val_corrects = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                val_corrects += torch.sum(preds == labels.data)
        val_acc = val_corrects.double() / len(val_loader.dataset)
        print(f"Epoch {epoch+1}/{epochs} | Train Acc: {epoch_acc:.4f} | Val Acc: {val_acc:.4f}")
    return model

model = train_model(model, criterion, optimizer, train_loader, val_loader, epochs=5)

# -----------------------------
# 6. Predict single image
# -----------------------------
def predict_image(image_path, model, transform, class_names):
    model.eval()
    image = Image.open(image_path)
    img = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(img)
        _, preds = torch.max(outputs, 1)
    return class_names[preds.item()]

# Example:
img_path = r"C:\Users\Abhi\Downloads\Plant_leaf_diseases_dataset_with_augmentation\PlantVillage\Tomato___Tomato_Yellow_Leaf_Curl_Virus\image (96).JPG"
prediction = predict_image(img_path, model, val_transforms, class_names)
print("Prediction:", prediction)
