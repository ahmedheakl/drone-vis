"""Yolov8 model implementation"""
from typing import Optional, Union
import logging
import time
from abc import abstractmethod

import numpy as np
from ultralytics import YOLO
import cv2

from dronevis.abstract.abstract_model import CVModel
from dronevis.utils.general import write_fps, device

_LOG = logging.getLogger(__name__)


class YOLOv8(CVModel):
    """YOLOv8 implementation with ultralytics model (inherits from CVModel)"""

    def __init__(self) -> None:
        self.model: Optional[YOLO] = None

    @abstractmethod
    def load_model(self, model_weights: str = "yolov8.pt"):
        pass

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Idel transformation for the input image, since yolov8 model does the transformations
        internaly during the inference.

        Args:
            image (np.ndarray): Input image

        Returns:
            np.ndarray: Same as the input image
        """
        return image

    def predict(
        self,
        image: np.ndarray,
        confidence: float = 0.5,
        track: bool = False,
    ) -> np.ndarray:
        """Run model inference on the provided image with the desired confidence

        Args:
            image (np.ndarray): Input image for inference
            confidence (float, optional): Confidence score representing what is threshold to
            be considered for detection. Defaults to 0.5.
            track (bool, optional): Whether to track the objects or not. Defaults to False.

        Returns:
            np.ndarray: Predicted image with bounding boxes drawn.
        """
        assert self.model, "Please load the model first"

        if track:
            results = self.model.track(image, stream=False, conf=confidence, device=device())
        else:
            results = self.model(image, stream=False, conf=confidence, device=device())
        return results[0].plot()

    def detect_webcam(
        self,
        video_index: Union[str, int] = 0,
        window_name="Cam Detection",
        track: bool = False,
    ):
        """Run web cam detection with yolov8 model

        Args:
            video_index (Union[str, int], optional): Index of the video stream. It can accept a
            camera index or a URL for remote sources. Defaults to 0.
            window_name (str, optional): Name of the cv2 window viewing the frames.
            Defaults to"Cam Detection".
            track (bool, optional): Whether to track the objects or not. Defaults to False.
        """
        cap = cv2.VideoCapture(video_index)
        if not cap.isOpened():
            _LOG.warning("Something is wrong with the video feed")

        while cap.isOpened():
            prev_time = time.time()
            _, frame = cap.read()
            image = self.predict(frame, track=track)
            fps = 1 / (time.time() - prev_time)
            cv2.imshow(window_name, write_fps(image, fps))

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()


class YOLOv8Detection(YOLOv8):
    """YOLOv8 model implementation for object detection"""

    def load_model(self, model_weights: str = "yolov8n.pt") -> None:
        """Load model weights

        Args:
            model_weights (str, optional): Path to model weight or the name of the official
            weights in the ultralytics website which will be downloaded automatically.
            Defaults to "yolov8.pt".
        """
        _LOG.info(f"Loading model weights with {device().upper()}")
        self.model = YOLO(model_weights)
        self.model.to(device())


class YOLOv8Segmentation(YOLOv8):
    """YOLOv8 model implementation for object segmentation"""

    def load_model(self, model_weights: str = "yolov8n-seg.pt") -> None:
        """Load model weights

        Args:
            model_weights (str, optional): Path to model weight or the name of the official
            weights in the ultralytics website which will be downloaded automatically.
            Defaults to "yolov8-seg.pt".
        """
        _LOG.info(f"Loading model weights with {device().upper()}")
        self.model = YOLO(model_weights)
        self.model.to(device())



class YOLOv8Pose(YOLOv8):
    """YOLOv8 model implementation for pose estimation"""

    def load_model(self, model_weights: str = "yolov8n-pose.pt") -> None:
        """Load model weights

        Args:
            model_weights (str, optional): Path to model weight or the name of the official
            weights in the ultralytics website which will be downloaded automatically.
            Defaults to "yolov8-pose.pt".
        """
        _LOG.info(f"Loading model weights with {device().upper()}")
        self.model = YOLO(model_weights)
        self.model.to(device())
