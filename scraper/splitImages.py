#splits images to train, test, and validate

from pathlib import Path
import numpy as np
import shutil as sh
from scrapebot import anime_dict

np.random.seed(42)

ROOT_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = ROOT_DIR / "Images"
DATASET_DIR = ROOT_DIR / "Dataset"

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15

for studio in anime_dict.keys():

    studio_dir = IMAGE_DIR / studio

    files = list(studio_dir.glob("*"))

    np.random.shuffle(files)

    n = len(files)

    train_end = int(n * TRAIN_RATIO)
    val_end = train_end + int(n * VAL_RATIO)

    splits = {
        "train": files[:train_end],
        "val": files[train_end:val_end],
        "test": files[val_end:],
    }

    for split_name, split_files in splits.items():

        split_dir = DATASET_DIR / split_name / studio

        split_dir.mkdir(parents=True, exist_ok=True)

        for filepath in split_files:

            sh.copy2(filepath, split_dir / filepath.name)

    print(f"{studio}: {len(splits['train'])} train / {len(splits['val'])} val / {len(splits['test'])} test")


