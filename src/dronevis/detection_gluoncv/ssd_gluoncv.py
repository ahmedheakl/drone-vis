from gluoncv import data
from dronevis.abstract.abstract_gluoncv_model import GluonCVModel
import mxnet as mx
import numpy as np


class SSD(GluonCVModel):
    def __init__(self) -> None:
        super(SSD, self).__init__(model_name="ssd")

    def load_model(self, model_path: str = "ssd_512_mobilenet1.0_voc_int8") -> None:
        """Loading SSD model

        The model is downloaded **only** the first time you use it,
        after that it is saved in the cache onto your OS.

        You can view a list of available model weights by invoking the ``get_model_options`` method:

        .. code-block:: python

            from droenvis.detection_gluoncv import SSD

            model = SSD()
            print(model.get_model_options())

        Args:
            model_name (str, optional): name of the model weights to be downloaded. Defaults to ``ssd_512_mobilenet1.0_voc_int8``.
        """
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
            imgs=mx.nd.array(img),
            short=self.short_size,
        )

    def load_and_transform_img(self, img_path):
        """Load img from hard-disk

        Args:
            img_path (str): path of the img on disk

        Returns:
            Tuple[mxnet.NDArray, np.ndarray]: A (1, 3, H, W) mxnet NDArray as
            input to network, and a numpy ndarray as original un-normalized
            color image for display
        """
        return data.transforms.presets.ssd.load_test(
            filenames=img_path,
            short=self.short_size,
        )
