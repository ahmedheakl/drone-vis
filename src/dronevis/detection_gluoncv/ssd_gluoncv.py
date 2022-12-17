from gluoncv import data
from dronevis.abstract.abstract_gluoncv_model import GluonCVModel
import mxnet as mx
import numpy as np


class SSD(GluonCVModel):
    def __init__(self, short_size: int = 512) -> None:
        super(SSD, self).__init__(model_name="ssd")

    def load_model(self, model_path: str = "ssd_512_mobilenet1.0_voc_int8") -> None:
        print("Loading SSD model ...")
        super().load_model(model_path=model_path)

    def transform_img(self, img: np.ndarray):
        """Transform the input image to have a short side size of 512

        Args:
            img (np.ndarray): input image

        Returns:
            Tuple[mxnet.NDArray, np.ndarray]: A (1, 3, H, W) mxnet NDArray as
            input to network, and a numpy ndarray as original un-normalized
            color image for display
        """
        return data.transforms.presets.ssd.transform_test(
            mx.nd.array(img), short=self.short_size
        )

    def load_and_transform_img(self, img_path):
        """Load img from harddisk

        Args:
            img_path (str): path of the img on disk

        Returns:
            (mx.NDArray, np.ndarray): input-ready image for inference,
            original image non-normalized
        """
        return data.transforms.presets.ssd.load_test(img_path, short=self.short_size)