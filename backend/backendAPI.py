from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai import predict_image
from pathlib import Path
import random
from fastapi.staticfiles import StaticFiles

IMAGE_DIR = Path(__file__).resolve().parent / "game image"


def get_random_image():
    images = list(IMAGE_DIR.rglob("*"))
    random_image = random.choice(images)

    real_studio = random_image.parent.name

    return random_image, real_studio


app = FastAPI()


app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

@app.get("/")
def home():
    return{
        "status":"Active"
    }

@app.get("/predict")
def predict():
    image_path, real_studio = get_random_image()

    studio = predict_image(image_path)

    if isinstance(studio, list):
        studio = studio[0]

    relative_path = image_path.relative_to(IMAGE_DIR)

    return {
        "image":  f"https://studioartnet.onrender.com/images/{relative_path.as_posix()}",
        "studio_prediction": studio,
        "real_studio": real_studio
    }


