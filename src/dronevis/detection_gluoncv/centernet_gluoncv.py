from dronevis.abstract.abstract_gluoncv_model import GluonCVModel
from gluoncv import data
import numpy as np
import mxnet as mx


class CenterNet(GluonCVModel):
    def __init__(self) -> None:
        super(CenterNet, self).__init__("center_net")
        
    def load_model(self, model_name: str = "center_net_resnet18_v1b_voc") -> None:
        print("Loading CenterNet model ...")
        super().load_model(model_name)
        
    def transform_img(self, img: np.ndarray):
        """Transform the input image to have a short side size of 512

        Args:
            img (np.ndarray): input image

        Returns:
            Tuple[mxnet.NDArray, np.ndarray]: A (1, 3, H, W) mxnet NDArray as input to network,
                                              and a numpy ndarray as original un-normalized color
                                              image for display
        """
        return data.transforms.presets.center_net.transform_test(
            mx.nd.array(img), short=self.short_size
        )

    def load_and_transform_img(self, img_path):
        """Load img from harddisk

        Args:
            img_path (str): path of the img on disk

        Returns:
            (mx.NDArray, np.ndarray): input-ready image for inference, original image non-normalized
        """
        return data.transforms.presets.center_net.load_test(img_path, short=self.short_size)