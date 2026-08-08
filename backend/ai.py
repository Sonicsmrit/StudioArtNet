import torch
from torchvision import transforms
import torchvision.models as models
import torch.nn as nn
from PIL import Image
from pathlib import Path

current_folder = Path(__file__).resolve().parent
best_model = current_folder / "best_model.pth"

model = models.resnet50(weights=None)
model.fc = nn.Linear(model.fc.in_features, 7)
model.load_state_dict(torch.load(best_model, map_location=torch.device('cpu')))

trans = transforms.Compose(
    [ 
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
            )
    ]
)

model = model.to("cpu")
model.eval()

studios={'Bones': 0, 
        'Kyoto Animation': 1, 
        'MAPPA': 2, 
        'Madhouse': 3, 
        'Trigger': 4, 
        'Wit Studio': 5, 
        'ufotable': 6}

def predict_image(image_path):
    image = Image.open(image_path).convert("RGB")

    image = trans(image)
    image = image.unsqueeze(0)

    with torch.no_grad():
        output = model(image)
        _, pred = torch.max(output, 1)

    studio_output = [key for key, val in studios.items() if val == pred.numpy()]

    return studio_output
