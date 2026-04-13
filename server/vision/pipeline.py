import os

import cv2

from paths import OUTPUT_PATH
from server.vision.annotator import draw_annotations
from server.vision.detector import ObjectDetector
from server.vision.estimators import estimate_stiffness
from server.utils.io import ensure_dir, save_json


class VisionPipeline:
    def __init__(self):
        self.detector = ObjectDetector()

    def process_image(self, image_path: str) -> dict:
        img, detections = self.detector.detect(image_path)

        for det in detections:
            det["stiffness"] = estimate_stiffness(det["class_name"])

        h, w = img.shape[:2]

        out = {
            "image": os.path.basename(image_path),
            "width": w,
            "height": h,
            "detections": detections
        }

        image_name = os.path.splitext(os.path.basename(image_path))[0]
        out_dir = os.path.join(OUTPUT_PATH, image_name)
        ensure_dir(out_dir)

        out_json = os.path.join(out_dir, f"{image_name}.json")
        out_img = os.path.join(out_dir, f"{image_name}.jpg")

        save_json(out_json, out)

        annotated = draw_annotations(img, detections)
        cv2.imwrite(out_img, annotated)

        print(f"Saved {len(detections)} detections to {out_json}")
        print(f"Annotated image saved to {out_img}")

        return out
