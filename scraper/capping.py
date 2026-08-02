# cap all folder image content to minimum folder image content(studio images)

import random
import os
from pathlib import Path
from scrapebot import anime_dict

random.seed(42)

ROOT_DIR = Path(__file__).resolve().parent.parent

IMAGE_DIR = ROOT_DIR / "Images"

TARGET_SIZE = 320


for studio in anime_dict.keys():
    
    studio_dir = IMAGE_DIR / studio
    all_files = list(studio_dir.glob("*"))

    before = len(all_files)

    if before <= TARGET_SIZE:
        print(f"{studio}: {before} (already at or below target, skipped)")
        continue

    keep = set(random.sample(all_files, TARGET_SIZE))
    to_remove = [f for f in all_files if f not in keep]

    for filepath in to_remove:
        os.remove(filepath)

    after = len(list(studio_dir.glob("*")))
    print(f"{studio}: {before} -> {after} (removed {len(to_remove)})")



