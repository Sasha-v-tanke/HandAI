name = vision / annotator.py
from typing import Any

import cv2
import numpy as np


def draw_annotations(img: np.ndarray, detections: list[dict[str, Any]]) -> np.ndarray:
    img_vis = img.copy()

    for det in detections:
        x1, y1, x2, y2 = map(int, det["bbox"])
        cls_name = det["class_name"]
        conf = det["confidence"]
        stiffness = det.get("stiffness", None)

        if stiffness is not None:
            label = f"{cls_name} {conf:.2f} S={stiffness:.2f}"
        else:
            label = f"{cls_name} {conf:.2f}"

        cv2.rectangle(img_vis, (x1, y1), (x2, y2), (0, 255, 0), 2)

        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        y_text_top = max(0, y1 - th - 6)

        cv2.rectangle(img_vis, (x1, y_text_top), (x1 + tw + 6, y1), (0, 255, 0), -1)
        cv2.putText(
            img_vis,
            label,
            (x1 + 3, y1 - 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )

        cx, cy = map(int, det["center"])
        cv2.circle(img_vis, (cx, cy), 3, (0, 0, 255), -1)

    return img_vis
