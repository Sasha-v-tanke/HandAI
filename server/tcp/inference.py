import json
from typing import Any

import cv2
import numpy as np

from server.vision.detector import ObjectDetector
from server.vision.estimators import estimate_stiffness


class InferenceService:
    def __init__(self):
        self.detector = ObjectDetector()

    def process_frame_bytes(self, frame_bytes: bytes) -> dict[str, Any]:
        """
        Принимает JPEG-байты, декодирует их, запускает детекцию и возвращает JSON-совместимый dict.
        """
        np_arr = np.frombuffer(frame_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            raise RuntimeError("Failed to decode image from bytes")

        h, w = img.shape[:2]
        detections = self.detector.detect_frame(img)

        for det in detections:
            det["stiffness"] = estimate_stiffness(det["class_name"])

        return {
            "width": w,
            "height": h,
            "detections": detections,
        }
