"""Huggingface depth estimation model implementation"""
from typing import Optional, Union
import math
import time
import logging

from transformers import pipeline
from transformers.pipelines.depth_estimation import DepthEstimationPipeline
from PIL import Image
import cv2
import numpy as np

from dronevis.abstract.abstract_model import CVModel
from dronevis.utils.general import device, write_fps


_LOG = logging.getLogger(__name__)


class DepthEstimator(CVModel):
    """Depth Estimation class with huggingface

    Source: https://huggingface.co/docs/transformers/tasks/monocular_depth_estimation
    """

    def __init__(self) -> None:
        self.net: Optional[DepthEstimationPipeline] = None

    def load_model(self, model_name: str = "vinvino02/glpn-nyu") -> None:
        """Load the model from huggingface model hub

        Args:
            model_name (str, optional): Model name to load. Defaults to "vinvino02/glpn-nyu".
        """
        self.net = pipeline(
            task="depth-estimation",
            model=model_name,
            device=device(),
        )

    def transform_img(self, image: Union[np.ndarray, Image.Image]) -> np.ndarray:
        """Idel transformation for the input image, since depth estimation model
        does the transformations internaly during the inference.

        Args:
            image (Union[np.ndarray, PIL.Image]): Input image

        Returns:
            np.ndarray: Same as the input image
        """
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        return image

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Run model inference on the provided image

        Args:
            image (np.ndarray): Input image for inference

        Returns:
            np.ndarray: Predicted image with bounding boxes drawn.
        """
        if self.net is None:
            _LOG.warning("Model not loaded. Loading default model ...")
            self.load_model()
            assert self.net

        image = self.transform_img(image)
        result = self.net(image)
        return np.array(result["depth"])

    def detect_webcam(
        self,
        video_index: Union[int, str] = 0,
        window_name: str = "Depth Estimation",
    ) -> None:
        cap = cv2.VideoCapture(video_index)
        if not cap.isOpened():
            _LOG.error("Cannot open camera")
            return

        while True:
            start = time.time()
            _, frame = cap.read()
            result = self.predict(frame)
            fps = max(1, 1 / (time.time() - start))
            cv2.imshow(window_name, write_fps(result, fps))
            if cv2.waitKey(math.ceil(fps)) == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
