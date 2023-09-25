"""Crowd counter model Implementation"""
from typing import Optional, Union
import logging

from ezcrowdcount.crowd_count import CrowdCounter as CrowdCounterModel
from ezcrowdcount import WEIGHTS_LINK
from ezcrowdcount.utils import download_file, preprocess, generate_density_map
from ezcrowdcount.network import load_net
import numpy as np
import cv2

from dronevis.abstract import CVModel
from dronevis.utils.general import device

_LOG = logging.getLogger(__name__)


class CrowdCounter(CVModel):
    """Crowd counter model"""

    def __init__(self) -> None:
        self.net: Optional[CrowdCounterModel] = None

    def load_model(self) -> None:
        """Load model weights"""
        self.net = CrowdCounterModel()
        model_path = download_file(WEIGHTS_LINK, "cmtl_shtechB_768.h5")
        load_net(model_path, self.net)
        self.net.eval()
        self.net.to(device=device())

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image

        Args:
            image (np.ndarray): Input image

        Returns:
            np.ndarray: Processed image
        """
        image = preprocess(image)
        return image

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Predict crowd count

        Args:
            image (np.ndarray): Input image

        Returns:
            np.ndarray: Crowd count
        """
        if self.net is None:
            _LOG.warning("Model is not loaded. Loading model...")
            self.load_model()
            assert self.net is not None

        image = self.transform_img(image)
        density_map = self.net(image)
        density_ndarr = density_map.cpu().detach().numpy()
        return density_ndarr

    def detect_webcam(
        self,
        video_index: Union[int, str] = 0,
        window_name: str = "Crowd Counter",
    ) -> None:
        """Run inference on webcam

        Args:
            video_index (Union[int, str], optional): Index of webcam. Defaults to 0.
            window_name (str, optional): Name of openCV window. Defaults to "Crowd Counter"
        """
        cap = cv2.VideoCapture(video_index)
        if not cap.isOpened():
            _LOG.error("Cannot open camera")
            return
        while True:
            ret, frame = cap.read()
            if not ret:
                _LOG.warning("Video stopped")
                break
            density_map = self.predict(frame)
            et_count = np.sum(density_map)
            density_map = generate_density_map(density_map)
            _LOG.warning("Estimated count: %d", et_count)
            cv2.imshow(window_name, density_map)
            if cv2.waitKey(1) == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
