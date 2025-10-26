import json
import os.path

import cv2
from ultralytics import YOLO

from config import CONF_THRESHOLD, IMG_SIZE, MODEL_NAME
from download import download_weights
from paths import MODELS_PATH, OUTPUT_PATH
from settings import map_stiffness
from utils import xyxy_to_center, draw_annotations


def detect_and_assign_stiffness(image_path: str,
                                conf_thresh: float = CONF_THRESHOLD,
                                image_size: int = IMG_SIZE) -> None:
    weights_path = os.path.join(MODELS_PATH, MODEL_NAME)
    if not os.path.exists(weights_path):
        download_weights()

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    model = YOLO(weights_path)

    results = model.predict(source=image_path, imgsz=image_size, conf=conf_thresh, verbose=False)

    names = model.names if hasattr(model, "names") else {}

    img = cv2.imread(image_path)
    if img is None:
        raise RuntimeError(f"Failed to read image: {image_path}")
    h, w = img.shape[:2]

    detections = []
    if len(results) == 0:
        print("No results returned by model.")
    else:
        r = results[0]
        if not hasattr(r, "boxes") or r.boxes is None:
            print("No boxes in result.")
        else:
            xyxy_arr = r.boxes.xyxy.cpu().numpy()  # N x 4
            confs = r.boxes.conf.cpu().numpy()  # N
            cls_ids = r.boxes.cls.cpu().numpy().astype(int)  # N

            for i in range(len(xyxy_arr)):
                x1, y1, x2, y2 = map(float, xyxy_arr[i])
                conf = float(confs[i])
                cls_id = int(cls_ids[i])
                class_name = names.get(cls_id, str(cls_id))

                cx, cy = xyxy_to_center((x1, y1, x2, y2))
                stiffness = map_stiffness(class_name)

                det = {
                    "class_id": cls_id,
                    "class_name": class_name,
                    "confidence": conf,
                    "bbox": [x1, y1, x2, y2],
                    "bbox_normalized": [x1 / w, y1 / h, x2 / w, y2 / h],
                    "center": [cx, cy],
                    "center_normalized": [cx / w, cy / h],
                    "stiffness": stiffness
                }
                detections.append(det)

    out = {
        "image": os.path.basename(image_path),
        "width": w,
        "height": h,
        "detections": detections
    }
    image_name = image_path.split("/")[-1].split(".")[0]
    os.makedirs(os.path.join(OUTPUT_PATH, image_name), exist_ok=True)
    out_json = os.path.join(OUTPUT_PATH, image_name, f"{image_name}.json")
    out_img = os.path.join(OUTPUT_PATH, image_name, f"{image_name}.jpg")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    annotated = draw_annotations(img, detections)
    cv2.imwrite(out_img, annotated)

    print(f"Saved {len(detections)} detections to {out_json}")
    print(f"Annotated image saved to {out_img}")
