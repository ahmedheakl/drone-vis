from torchvision.models.detection import (
    ssdlite320_mobilenet_v3_large,
    SSDLite320_MobileNet_V3_Large_Weights,
)
from dronevis.abstract.abstract_torch_model import TorchDetectionModel


class SSD(TorchDetectionModel):
    def __init__(self) -> None:
        """Initialize SSD model and load weights"""
        super(SSD, self).__init__()        
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
    model = SSD()
    model.load_model()
    model.detect_webcam()
