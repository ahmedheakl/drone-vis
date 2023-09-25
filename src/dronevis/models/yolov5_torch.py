"""Implementation of CVModel for YOLOv5 used for object detection"""
from typing import Union
import os
import time
import logging
import getpass
import torch
import cv2
import numpy as np

from dronevis.utils.general import write_fps
from dronevis.abstract import CVModel

_LOG = logging.getLogger(__name__)


class YOLOv5(CVModel):
    """YOLOv5 implementation with torch hub model (inherits from CVModel).

    For more details see `YOLOv5 <https://pytorch.org/hub/ultralytics_yolov5>`_.
    """

    local_name = "ultralytics_yolov5_master"
    remote_name = "ultralytics/yolov5"
    model_local_path = f"/home/{getpass.getuser()}/.cache/torch/hub/{local_name}"
    model_source = "local"
    model_name = "yolov5s"

    def __init__(self) -> None:
        """Initialize local path"""
        self.net = None

    def load_model(self) -> None:
        """Load model from PyTorchHub"""
        _LOG.info("Loading YOLOv5 Torch model ...")
        if os.path.exists(self.model_local_path):
            self.net = torch.hub.load(
                self.model_local_path,
                model=self.model_name,
                source=self.model_source,
            )
        else:
            self.net = torch.hub.load(self.remote_name, self.model_name)
        _LOG.info("Loaded YOLOv5 Torch model")

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Idle transformation.

        **Implemented just for code integrity**


        Args:
            image (np.ndarray): input image

        Returns:
            np.ndarray: output image
        """
        return image

    def predict(self, image: np.ndarray):
        """Run model inference on input image and return
        bouding boxes along with object names

        Args:
            image (np.array): input image

        Returns:
            torch.hub.models.self.common.Detections: detections object
        """
        if self.net is None:
            _LOG.warning("Model not loaded. Loading default model...")
            self.load_model()
            assert self.net
        return self.net(image).render()[0]

    def detect_webcam(
        self,
        video_index: Union[str, int] = 0,
        window_name: str = "YOLOv5 Detection",
    ) -> None:
        """Start webcam detection from video_index
        *(to quit running this function press 'q')*

        The stream is retrieved and decoded using `opencv library <https://opencv.org/>`_.

        Args:
            video_index (Union[str, int], optional): index of video stream device.
            Defaults to 0 (webcam).
            window_name (str, optional): name of cv2 window. Defaults to "Cam Detection".
        """
        cap: cv2.VideoCapture = cv2.VideoCapture(video_index)
        if not cap.isOpened():
            _LOG.error("Cannot open camera")
            return
        prev_time = 0.0
        while True:
            _, frame = cap.read()

            image = self.predict(frame)
            cur_time = time.time()
            fps = 1 / (cur_time - prev_time)
            cv2.imshow(window_name, write_fps(image, fps))
            prev_time = cur_time
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()
        cap.release()
