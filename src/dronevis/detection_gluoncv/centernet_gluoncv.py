from dronevis.abstract.abstract_gluoncv_model import GluonCVModel
from gluoncv import data
import numpy as np
import mxnet as mx


class CenterNet(GluonCVModel):
    def __init__(self) -> None:
        super(CenterNet, self).__init__("center_net")

    def load_model(self, model_name: str = "center_net_resnet18_v1b_voc") -> None:
        """Loading centernet model

        The model is downloaded **only** the first time you use it,
        after that it is saved in the cache onto your OS.

        You can view a list of available model weights by invoking the ``get_model_options`` method:

        .. code-block:: python

            from droenvis.detection_gluoncv import CenterNet

            model = CenterNet()
            print(model.get_model_options())

        Args:
            model_name (str, optional): name of the model weights to be downloaded. Defaults to ``center_net_resnet18_v1b_voc``.
        """
        print("Loading CenterNet model ...")
        super().load_model(model_name)

    def transform_img(self, img: np.ndarray):
        """Transform the input image to have a short side size of 512

        Args:
            img (numpy.ndarray): input image

        Returns:
            Tuple[mxnet.NDArray, numpy.ndarray]: A (1, 3, H, W) mxnet NDArray as input to network,
            and a numpy ndarray as original un-normalized color
            image for display
        """
        return data.transforms.presets.center_net.transform_test(
            imgs=mx.nd.array(img),
            short=self.short_size
        )

    def load_and_transform_img(self, img_path: str):
        """Load img from harddisk

        Args:
            img_path (str): path of the img on disk

        Returns:
            Tuple[mxnet.NDArray, numpy.ndarray]: A (1, 3, H, W) mxnet NDArray as input to network,
            and a numpy ndarray as original un-normalized color
            image for display
        """
        return data.transforms.presets.center_net.load_test(
            filenames=img_path,
            short=self.short_size
        )
