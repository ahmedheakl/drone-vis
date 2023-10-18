"""Implementation for the CNN Face Detection model"""
from typing import Tuple, Optional
import logging
import time

import dlib
import cv2
import numpy as np

from dronevis.abstract import CVModel
from dronevis.config.general import MODELS_URLS
from dronevis.utils.general import download_file, write_fps

_LOG = logging.getLogger(__name__)


class CNNFaceDetection(CVModel):
    """CNN Face Detection model"""

    def __init__(self) -> None:
        self.net: Optional[dlib.dlib_pybind11.cnn_face_detection_model_v1] = None

    def load_model(self) -> None:
        """Load model weights"""
        model_weights = download_file(*MODELS_URLS["cnn_face_detection"])
        self.net = dlib.cnn_face_detection_model_v1(model_weights)

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Run image transformation

        Args:
            image (np.ndarray): Input image

        Returns:
            np.ndarray: Transformed image
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Run model inference on the image

        Args:
            image (np.ndarray): Input image

        Returns:
            np.ndarray: Image withe face annotations
        """
        if self.net is None:
            _LOG.error("Model is not loaded. Loading default model...")
            self.load_model()
            assert self.net, "Model could not be loaded"

        processed_image = self.transform_img(image)
        green_color = (0, 255, 0)
        thickness = 2
        bboxes = self.net(processed_image, 0)
        for bbox in bboxes:
            cv2.rectangle(
                image,
                (bbox.rect.left(), bbox.rect.top()),
                (bbox.rect.right(), bbox.rect.bottom()),
                green_color,
                thickness,
            )

        return image

    def detect_webcam(
        self,
        video_index: Tuple[int, str] = 0,
        window_name="CNN Face Detection",
    ) -> None:
        """Detect faces on webcam

        Args:
            video_index (Tuple[int, str], optional): Video index or path. Defaults to 0.
            window_name (str, optional): Window name. Defaults to "CNN Face Detection".
        """
        cap = cv2.VideoCapture(video_index)
        if not cap.isOpened():
            _LOG.error("Could not open video capture")
            return

        while True:
            ret, frame = cap.read()
            prev_time = time.perf_counter()
            if not ret:
                _LOG.error("Could not read frame")
                break

            frame = self.predict(frame)
            fps = 1 / (time.perf_counter() - prev_time)
            cv2.imshow(window_name, write_fps(frame, fps))
            if cv2.waitKey(1) == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
