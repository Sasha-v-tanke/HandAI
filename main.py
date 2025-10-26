from paths import TEST_IMAGES_PATH
from process import detect_and_assign_stiffness
from utils import load_all_images

if __name__ == "__main__":
    images = load_all_images(TEST_IMAGES_PATH)
    for image in images:
        detect_and_assign_stiffness(image)
