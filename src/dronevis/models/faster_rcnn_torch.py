"""Implementation for TorchDetecionModel for FasterRCNN"""
import logging
from torchvision.models.detection import (
    fasterrcnn_mobilenet_v3_large_320_fpn,
    FasterRCNN_MobileNet_V3_Large_320_FPN_Weights,
)
from dronevis.abstract.abstract_torch_model import TorchDetectionModel

_LOG = logging.getLogger(__name__)


class FasterRCNN(TorchDetectionModel):
    """FasterRCNN model implementation for object detection/recognition"""

    def __init__(self) -> None:
        """Initialize faster R-CNN model"""
        super().__init__()
        self.weights = FasterRCNN_MobileNet_V3_Large_320_FPN_Weights.DEFAULT
        self.transform = self.weights.transforms()

    def load_model(self) -> None:
        """Load model from PyTorchHub

        .. note::

            Default weights used are ``fasterrcnn_mobilenet_v3_large_320_fpn``.
        """
        _LOG.info("Loading Faster R-CNN model ...")
        self.net = (
            fasterrcnn_mobilenet_v3_large_320_fpn(weights=self.weights)
            .eval()
            .to(self.device)
        )
        _LOG.info("Loadded Faster R-CNN model")
