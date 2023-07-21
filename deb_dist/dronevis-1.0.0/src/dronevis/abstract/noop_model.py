"""Implementation for an idle computer vision model"""
import numpy as np

from dronevis.abstract import CVModel


class NOOPModel(CVModel):
    """Idel computer vision model"""

    def load_model(self):
        """Load weights"""

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Transform input image

        Args:
            image (np.ndarray): Input image

        Returns:
            _type_: Same image
        """
        return image

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Run model inference on input image"""
        return image

    def detect_webcam(
        self,
        video_index: int,
        window_name: str = "Cam Detection",
    ) -> None:
        """Run inference on webcam stream

        Args:
            video_index (int): Index of the video streaming device
            window_name (str, optional): Name of stream window.
            Defaults to "Cam Detection".
        """
