from paths import TEST_IMAGES_PATH
from utils.io import load_all_images
from vision.pipeline import VisionPipeline


def main() -> None:
    pipeline = VisionPipeline()

    images = load_all_images(TEST_IMAGES_PATH)
    if not images:
        print(f"No images found in {TEST_IMAGES_PATH}")
        return

    for image in images:
        pipeline.process_image(image)


if __name__ == "__main__":
    main()
