"""Haar Face Detection model"""
from typing import Optional, Tuple, Union
import logging
import time

import cv2
import numpy as np

from dronevis.abstract import CVModel
from dronevis.utils.general import write_fps

_LOG = logging.getLogger(__name__)


class HaarFaceDetection(CVModel):
    """Face detection class with Haar Cascades

    Paper: Rapid Object Detection using a Boosted Cascade
    of Simple Features
    """

    def __init__(
        self,
        min_neighbours: int = 5,
        min_size: Tuple[int, int] = (10, 10),
        scale_factor: float = 1.1,
    ) -> None:
        """Initialize model instance

        Args:
            min_neighbours (int, optional): Number of neighbours each candidate. Defaults to 5.
            min_size (Tuple[int, int], optional): Min box size for each face. Defaults to (10, 10).
            scale_factor (float, optional): Scale the image. Defaults to 1.1.
        """
        self.net = None
        self.min_neighbours = min_neighbours
        self.min_size = min_size
        self.scale_factor = scale_factor

    def load_model(self, model_name: Optional[str] = None) -> None:
        """Laod model weights"""
        if model_name is None:
            model_name = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

        self.net = cv2.CascadeClassifier(model_name)

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Run image transformation"""
        img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return img_grey

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Run model inference on the image

        Args:
            image (np.ndarray): Input image

        Returns:
            np.ndarray: Image withe face annotations
        """
        if self.net is None:
            _LOG.info("Model not loaded. Loading default model")
            self.load_model()
            assert self.net, "Model not loaded properly"

        img_grey = self.transform_img(image)
        faces = self.net.detectMultiScale(
            img_grey,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbours,
            minSize=self.min_size,
        )

        for x, y, w, h in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return image

    def detect_webcam(self, video_index: Union[int, str] = 0, window_name="Haar Face"):
        cap = cv2.VideoCapture(video_index)
        if not cap.isOpened():
            _LOG.error("Could not open video capture")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            prev_time = time.perf_counter()
            frame = self.predict(frame)
            fps = 1 / (time.perf_counter() - prev_time)
            cv2.imshow(window_name, write_fps(frame, fps))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
