import glob
import json
import os


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def load_all_images(path: str, everywhere: bool = False) -> list[str]:
    images = []
    extensions = [".jpg", ".jpeg", ".png", ".webp"]

    for ext in extensions:
        pattern = "**/*" + ext if everywhere else "*" + ext
        images.extend(glob.glob(os.path.join(path, pattern), recursive=everywhere))

    return images


def save_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
