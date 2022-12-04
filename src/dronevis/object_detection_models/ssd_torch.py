import torch
import time
from typing import List
import cv2
import numpy as np
from PIL import Image
from dronevis.config.config import COCO_NAMES
from torchvision.transforms.functional import to_pil_image
from torchvision.models.detection import (
    ssdlite320_mobilenet_v3_large,
    SSDLite320_MobileNet_V3_Large_Weights,
)
from dronevis.object_detection_models import TorchDetectionModel


class SSDTorch(TorchDetectionModel):
    def __init__(self) -> None:
        """Initialize faster R-CNN model"""
        super(SSDTorch, self).__init__()        
        self.weights = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
        self.transform = self.weights.transforms()


    def load_model(self):
        """Load model from PyTorchHub

        Args:
            model_path (str, optional): no need to use it, only for integrity with absract class. Defaults to None.
        """
        print("Loading SSD Torch model ...")
        self.net = ssdlite320_mobilenet_v3_large(weights=self.weights)
        self.net = self.net.eval().to(self.device)

if __name__ == "__main__":
    model = SSDTorch()
    model.load_model()
    model.detect_webcam()
