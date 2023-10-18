"""HOG face detector model"""
import logging
from typing import Tuple
import time

import dlib
import numpy as np
import cv2

from dronevis.abstract import CVModel
from dronevis.utils.general import write_fps

_LOG = logging.getLogger(__name__)


class HOGFaceDetection(CVModel):
    """HOG Face Detection model"""

    def __init__(self):
        self.net = None
        self.net_cuda = None

    def load_model(self) -> None:
        """Load model weights"""
        self.net = dlib.get_frontal_face_detector()

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Run image transformation"""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Run model inference on the image

        Args:
            image (np.ndarray): Input image

        Returns:
            np.ndarray: Image withe face annotations
        """
        if self.net is None:
            _LOG.warning("Model is not loaded. Loading default model...")
            self.load_model()
            assert self.net, "Model could not be loaded"

        green_color = (0, 255, 0)
        thickness = 2
        bboxes = self.net(image, 0)
        for bbox in bboxes:
            cv2.rectangle(
                image,
                (bbox.left(), bbox.top()),
                (bbox.right(), bbox.bottom()),
                green_color,
                thickness,
            )

        return image

    def detect_webcam(
        self, video_index: Tuple[int, str] = 0, window_name="HOG Face Detection"
    ):
        cap = cv2.VideoCapture(video_index)

        if not cap.isOpened():
            _LOG.error("Could not open video capture")
            return

        while True:
            ret, frame = cap.read()
            prev_time = time.perf_counter()
            if not ret:
                _LOG.error("Cannot receive frame. Exiting...")
                break

            frame = self.predict(frame)
            fps = 1 / (time.perf_counter() - prev_time)
            cv2.imshow(window_name, write_fps(frame, fps))

            if cv2.waitKey(1) == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
