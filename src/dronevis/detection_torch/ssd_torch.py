"""Implementation of TorchDetectionModel interface for SSD object detection model"""
import logging
from torchvision.models.detection import (
    ssdlite320_mobilenet_v3_large,
    SSDLite320_MobileNet_V3_Large_Weights,
)
from dronevis.abstract.abstract_torch_model import TorchDetectionModel

_LOG = logging.getLogger(__name__)


class SSD(TorchDetectionModel):
    """Single shot detector model implementation for object
    detection/recognition using torchvision pre-trained models"""

    def __init__(self) -> None:
        """Initialize SSD model and load weights"""
        super().__init__()
        self.weights = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
        self.transform = self.weights.transforms()

    def load_model(self):
        """Load model from PyTorchHub

        .. note::

            Default weights used are ``ssdlite320_mobilenet_v3_large``.
        """
        _LOG.info("Loading SSD Torch model ...")
        self.net = ssdlite320_mobilenet_v3_large(weights=self.weights)
        self.net = self.net.eval().to(self.device)
        _LOG.info("Loaded SSD Torch model")
