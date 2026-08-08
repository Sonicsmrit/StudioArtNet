from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai import predict_image
from pathlib import Path
import random

IMAGE_DIR = Path(__file__).resolve().parent.parent / "Test Data"

def get_random_image():
    images = list(IMAGE_DIR.rglob("*"))
    random_image = random.choice(images)

    real_studio = random_image.parent.name

    return random_image, real_studio


app = FastAPI()


app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return{
        "status":"Active"
    }

@app.get("/predict")
def predict():
    image_path, real_studio = get_random_image()

    studio = predict_image(image_path)

    return {
        "image": image_path.name,
        "studio": studio,
        "real studio": real_studio
    }


