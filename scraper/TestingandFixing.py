from pathlib import Path
from scrapebot import anime_dict
from imagededup.methods import PHash
import os

ROOT_DIR = Path(__file__).resolve().parent.parent

IMAGE_DIR = ROOT_DIR / "Images"

def dedup_studio(studio_dir):
    phasher = PHash()
    encoding = phasher.encode_images(image_dir=studio_dir)
    duplicates_to_remove = phasher.find_duplicates_to_remove(encoding_map=encoding, max_distance_threshold=10)

    for imagename in duplicates_to_remove:
        filepath = studio_dir/imagename
        os.remove(filepath)

    return len(duplicates_to_remove)


if __name__ == "__main__":

    for studio in anime_dict.keys():

        Studio_dir = IMAGE_DIR / studio

        before = len(list(Studio_dir.glob("*")))

        removed = dedup_studio(studio_dir=Studio_dir)

        after = before - removed

        print(f"{studio}: {before} -> {after} (removed {removed})")


for studio in anime_dict.keys():

    Studio_dir = IMAGE_DIR / studio

    img = len(list(Studio_dir.glob("*")))

    print(f"{studio} images: {img}")

