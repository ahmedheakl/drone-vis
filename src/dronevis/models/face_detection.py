"""Implementation for face detection from mediapipe"""
from typing import Union
import time

import cv2
import mediapipe as mp
import numpy as np

from dronevis.abstract import CVModel
from dronevis.utils.general import write_fps


class FaceDetectModel(CVModel):
    """Face detection class with mediapipe

    This class inherits from base class ``CVModel``, and implements
    its abstract methods for code integrity.
    """

    def __init__(self, confidence: float = 0.6) -> None:
        """Construct model instance

        Args:
            confidence (float, optional): threshold for detection,
            **input is a probability [0, 1]**.
            Defaults to 0.5.
        """
        if not isinstance(confidence, (int, float)):
            raise TypeError("Confidence must be a float or int")

        assert 0.0 <= confidence <= 1.0, "Confidence must be a score between 0 and 1"
        self.face_detection = mp.solutions.face_detection.FaceDetection(confidence)
        self.mp_drawing = mp.solutions.drawing_utils

    def load_model(self) -> None:
        """Load model from memory"""

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Idle transformation of the image"""
        return image

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Run model inference on input image and output face detection
        keypoints.

        Args:
            img (np.array): input image (assumed to be non-transformed)

        Returns:
            np.array: output image with keypoints drawn
        """
        results = self.face_detection.process(image)
        if results.detections:
            for detection in results.detections:
                self.mp_drawing.draw_detection(image, detection)

        return image

    def detect_webcam(
        self,
        video_index: Union[int, str] = 0,
        window_name: str = "Face Detection",
    ) -> None:
        """Run webcam (or any video streaming device) with face detection module

        Args:
            video_index (Union[int, str], optional): index of video device. can be an ``IP``
            or ``video_path``. Defaults to 0.
            window_name (str, optional): name of opencv window. Defaults to "Face Detection".
        """
        cap = cv2.VideoCapture(video_index)
        while True:
            _, frame = cap.read()
            prev_time = time.perf_counter()
            image = self.predict(frame)
            fps = 1 / (time.perf_counter() - prev_time)
            cv2.imshow(window_name, write_fps(image, fps))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()
        cap.release()
