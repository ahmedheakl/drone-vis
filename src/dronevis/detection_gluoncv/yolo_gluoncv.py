from dronevis.abstract.abstract_gluoncv_model import GluonCVModel
from gluoncv import data
import mxnet as mx
import numpy as np


class YOLO(GluonCVModel):
    def __init__(self) -> None:
        super(YOLO, self).__init__(model_name="yolo")

    def load_model(self, model_path: str = "yolo3_darknet53_voc"):
        print("Loading YOLO model ...")
        super().load_model(model_path=model_path)

    def transform_img(self, img: np.ndarray):
        """Transform the input img according to YOLO transforms

        Args:
            img (np.ndarray): input numpy array image

        Returns:
            (mx.NDArray, np.ndarray): input-ready image for inference, original image non-normalized
        """
        return data.transforms.presets.yolo.transform_test(
            mx.nd.array(img), short=self.short_size
        )

    def load_and_transform_img(self, img_path):
        """Load img from harddisk

        Args:
            img_path (str): path of the img on disk

        Returns:
            (mx.NDArray, np.ndarray): input-ready image for inference, original image non-normalized
        """
        return data.transforms.presets.yolo.load_test(img_path, short=self.short_size)
