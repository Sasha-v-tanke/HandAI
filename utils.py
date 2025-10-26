import glob
import os
from typing import Any

import cv2
import numpy as np

from paths import DATA_PATH


def xyxy_to_center(xyxy: tuple[float, float, float, float]) -> tuple[float, float]:
    x1, y1, x2, y2 = xyxy
    cx = (x1 + x2) / 2.0
    cy = (y1 + y2) / 2.0
    return cx, cy


def draw_annotations(img: np.ndarray, detections: list[dict[str, Any]]) -> np.ndarray:
    img_vis = img.copy()
    h, w = img_vis.shape[:2]
    for det in detections:
        x1, y1, x2, y2 = map(int, det["bbox"])
        cls_name = det["class_name"]
        conf = det["confidence"]
        stiffness = det["stiffness"]
        label = f"{cls_name} {conf:.2f} S={stiffness}"

        cv2.rectangle(img_vis, (x1, y1), (x2, y2), (0, 255, 0), 2)

        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img_vis, (x1, y1 - th - 6), (x1 + tw + 6, y1), (0, 255, 0), -1)
        cv2.putText(img_vis, label, (x1 + 3, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

        cx, cy = map(int, det["center"])
        cv2.circle(img_vis, (cx, cy), 3, (0, 0, 255), -1)
    return img_vis


def load_all_images(path: str, everywhere=False) -> list[str]:
    images = []
    print(path)
    extensions = [".jpg", ".jpeg", ".png", '.webp']
    for ext in extensions:
        extension = "**/*" + ext if everywhere else "*" + ext
        images.extend(glob.glob(os.path.join(path, extension)))
    return images


if __name__ == "__main__":
    assert len(load_all_images(DATA_PATH, everywhere=True)) > 0
    print('Found images:', len(load_all_images(DATA_PATH, everywhere=True)))
