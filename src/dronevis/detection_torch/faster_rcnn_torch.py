from torchvision.models.detection import (
    fasterrcnn_mobilenet_v3_large_320_fpn,
    FasterRCNN_MobileNet_V3_Large_320_FPN_Weights
)
from dronevis.abstract.abstract_torch_model import TorchDetectionModel

class FasterRCNN(TorchDetectionModel):
    def __init__(self) -> None:
        """Initialize faster R-CNN model"""
        super(FasterRCNN, self).__init__()
        self.weights = FasterRCNN_MobileNet_V3_Large_320_FPN_Weights.DEFAULT
        self.transform = self.weights.transforms()


    def load_model(self) -> None:
        """Load model from PyTorchHub
        
        .. note::
            
            Default weights used are ``fasterrcnn_mobilenet_v3_large_320_fpn``.
        """
        print("Loading Faster R-CNN model ...")
        self.net = fasterrcnn_mobilenet_v3_large_320_fpn(weights=self.weights)
        self.net = self.net.eval().to(self.device)
