import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data")
TEST_IMAGES_PATH = os.path.join(DATA_PATH, "data/test")
MODELS_PATH = os.path.join(BASE_DIR, "models")
OUTPUT_PATH = os.path.join(BASE_DIR, "output")

os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(TEST_IMAGES_PATH, exist_ok=True)
os.makedirs(MODELS_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)
