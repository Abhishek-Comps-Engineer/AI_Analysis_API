import torch
from torchvision import transforms
from PIL import Image
import os
import torch.nn as nn
from torchvision import models


road_types = ["Asphalt", "Dirt", "Gravel", "Highway", "Urban"]
road_conditions = ["Smooth", "Potholes", "Cracks", "Wet", "Damaged"]

class RoadMultiTaskModel(nn.Module):
    def __init__(self):
        super().__init__()
        backbone = models.mobilenet_v2(pretrained=True)
        in_features = backbone.last_channel
        self.backbone = backbone.features
        self.pool = nn.AdaptiveAvgPool2d((1,1))
        self.road_type_head = nn.Linear(in_features, len(road_types))
        self.condition_head = nn.Linear(in_features, len(road_conditions))

    def forward(self, x):
        x = self.backbone(x)
        x = self.pool(x)
        x = torch.flatten(x, 1)
        return self.road_type_head(x), self.condition_head(x)
