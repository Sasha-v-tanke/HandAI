import cv2


class Camera:
    def __init__(self, camera_index: int = 0, width: int | None = None, height: int | None = None):
        self.cap = cv2.VideoCapture(camera_index)

        if width is not None:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height is not None:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera index {camera_index}")

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame from camera")
        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
