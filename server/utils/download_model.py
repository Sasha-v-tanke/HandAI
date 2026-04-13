import os
import shutil

from ultralytics import YOLO

from server.config import MODEL_NAME
from paths import MODELS_PATH


def download_weights() -> None:
    model = YOLO(MODEL_NAME)
    os.makedirs(MODELS_PATH, exist_ok=True)
    shutil.move(model.ckpt_path, os.path.join(MODELS_PATH, MODEL_NAME))
    print(f"Model saved to {os.path.join(MODELS_PATH, MODEL_NAME)}")


if __name__ == "__main__":
    download_weights()
