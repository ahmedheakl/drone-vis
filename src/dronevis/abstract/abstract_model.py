"""Interface for computer vision model. All models implemented should be
an implementation of this interface for code integrity"""
from abc import ABC, abstractmethod
import numpy as np


class CVModel(ABC):
    """Base class for creating custom comptervision models.

    To use the abstract class just inherit it, and override
    the abstract method.

    Main methods:

    1. ``load_model``
    Load model weights from web or cache.
    You only need to download the model weights once,
    and they will be stored and loaded automatically each time you use them later.

    2. ``predict``
    Run model inference on input image
    You don't have to transform the image before the inference, input images will be
    transformed automatically.

    3. ``transform_img``
    Transform input image according to models transformations

    4. ``detect_webcam``
    Start webcam (or any camera) detection
    """

    @abstractmethod
    def load_model(self):
        """Load model weights from disk"""

    @abstractmethod
    def predict(self, image) -> np.ndarray:
        """Get predictions for inference on input image"""

    @abstractmethod
    def transform_img(self, image):
        """Transform input image using model transformations"""

    @abstractmethod
    def detect_webcam(self, video_index: int, window_name="Cam Detection"):
        """Run model on a video stream from the webcam

        Args:
            video_index (int): Index of the camera/video device to retrieve stream
            window_name (str, optional): Name of openCV window for running the mpdel.
            Defaults to "Cam Detection".
        """
