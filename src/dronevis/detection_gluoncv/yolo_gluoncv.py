from dronevis.abstract.abstract_gluoncv_model import GluonCVModel
from gluoncv import data
import mxnet as mx
import numpy as np


class YOLO(GluonCVModel):
    def __init__(self) -> None:
        super(YOLO, self).__init__(model_name="yolo")

    def load_model(self, model_path: str = "yolo3_darknet53_voc"):
        """Loading YOLO model

        The model is downloaded **only** the first time you use it,
        after that it is saved in the cache onto your OS.

        You can view a list of available model weights by invoking the ``get_model_options`` method:

        .. code-block:: python

            from droenvis.detection_gluoncv import YOLO

            model = YOLO()
            print(model.get_model_options())

        Args:
            model_name (str, optional): name of the model weights to be downloaded. Defaults to ``yolo3_darknet53_voc``.
        """
        print("Loading YOLO model ...")
        super().load_model(model_path=model_path)

    def transform_img(self, img: np.ndarray):
        """Transform the input img according to YOLO transforms

        Args:
            img (np.ndarray): input numpy array image

        Returns:
            Tuple[mxnet.NDArray, np.ndarray]: A (1, 3, H, W) mxnet NDArray as
            input to network, and a numpy ndarray as original un-normalized
            color image for display
        """
        return data.transforms.presets.yolo.transform_test(
            imgs=mx.nd.array(img),
            short=self.short_size,
        )

    def load_and_transform_img(self, img_path):
        """Load img from harddisk

        Args:
            img_path (str): path of the img on disk

        Returns:
            Tuple[mxnet.NDArray, np.ndarray]: A (1, 3, H, W) mxnet NDArray as
            input to network, and a numpy ndarray as original un-normalized
            color image for display
        """
        return data.transforms.presets.yolo.load_test(
            filenames=img_path,
            short=self.short_size,
        )
