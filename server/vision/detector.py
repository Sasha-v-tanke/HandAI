import os
from typing import Any

import cv2
import numpy as np
from ultralytics import YOLO

from config import CONF_THRESHOLD, IMG_SIZE, MODEL_NAME
from download import download_weights
from paths import MODELS_PATH
from utils.geometry import xyxy_to_center


class ObjectDetector:
    def __init__(
            self,
            model_name: str = MODEL_NAME,
            conf_thresh: float = CONF_THRESHOLD,
            img_size: int = IMG_SIZE,
    ):
        self.model_name = model_name
        self.conf_thresh = conf_thresh
        self.img_size = img_size
        self.weights_path = os.path.join(MODELS_PATH, self.model_name)
        self.model = None

        if not os.path.exists(self.weights_path):
            download_weights()

        self._load_model()

    def _load_model(self) -> None:
        self.model = YOLO(self.weights_path)

    def detect_frame(self, img: np.ndarray) -> list[dict[str, Any]]:
        h, w = img.shape[:2]

        results = self.model.predict(
            source=img,
            imgsz=self.img_size,
            conf=self.conf_thresh,
            verbose=False,
        )

        detections: list[dict[str, Any]] = []
        names = self.model.names if hasattr(self.model, "names") else {}

        if len(results) > 0:
            r = results[0]
            if hasattr(r, "boxes") and r.boxes is not None:
                xyxy_arr = r.boxes.xyxy.cpu().numpy()
                confs = r.boxes.conf.cpu().numpy()
                cls_ids = r.boxes.cls.cpu().numpy().astype(int)

                for i in range(len(xyxy_arr)):
                    x1, y1, x2, y2 = map(float, xyxy_arr[i])
                    conf = float(confs[i])
                    cls_id = int(cls_ids[i])
                    class_name = names.get(cls_id, str(cls_id))
                    cx, cy = xyxy_to_center((x1, y1, x2, y2))

                    detections.append(
                        {
                            "class_id": cls_id,
                            "class_name": class_name,
                            "confidence": conf,
                            "bbox": [x1, y1, x2, y2],
                            "bbox_normalized": [x1 / w, y1 / h, x2 / w, y2 / h],
                            "center": [cx, cy],
                            "center_normalized": [cx / w, cy / h],
                        }
                    )

        return detections
