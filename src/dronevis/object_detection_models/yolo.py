from dronevis.object_detection_models.abstract_model import CVModel
from gluoncv import data, utils, model_zoo
import mxnet as mx
import numpy as np
import matplotlib.pyplot as plt

class Yolo(CVModel):
    def __init__(self, short_size: int = 512) -> None:
        """Initialize Yolo model

        Args:
            short_size (int, optional): dim of the shorterd side. Defaults to 512.
        """
        self.short_size = short_size
        self.net = None
        self.class_IDs = None
        self.scores = None
        self.bounding_boxes = None

    def load_model(self, model_path: str = "yolo3_darknet53_voc"):
        """Load the YOLO model from gluoncv
        Run ``get_model_options`` to see available options

        Args:
            model_path (str): name of the model in the model zoo
        """
        self.net = model_zoo.get_model(name=model_path, pretrained=True)

    def transform_img(self, img):
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

    def predict(self, img, img_data):
        """Generate predictions along with a labelled img

        Args:
            img_data: input to the network
            img: normal img with un-normalized colors

        Returns:
            classesID, scores, bounding boxes, and the labelled img
        """
        assert (
            self.net
        ), "You need to load the model first. Please run load_model method."
        self.class_IDs, self.scores, self.bounding_boxes = self.net(img_data)
        labelled_img = utils.viz.cv_plot_bbox(
            img,
            self.bounding_boxes[0],
            self.scores[0],
            self.class_IDs[0],
            class_names=self.net.classes,
        )
        return labelled_img

    def add_bounding_box(self, img: np.ndarray):
        """Add bouding boxes along with their scores to input image

        Args:
            img (np.ndarray): input image

        Returns:
            np.ndarray: labelled image
        """
        assert (
            self.net
        ), "You need to load the model first. Please run load_model method."

        # fmt: off
        assert self.bounding_boxes is not None, "You need to inference the model first. Run predict func."
        assert self.scores is not None, "You need to inference the model first. Run predict func."
        assert self.class_IDs is not None, "You need to inference the model first. Run predict func."

        return utils.viz.cv_plot_bbox(
            img,
            self.bounding_boxes[0],
            self.scores[0],
            self.class_IDs[0],
            class_names=self.net.classes,
        )
    def plot_bounding_box(self, img):
        assert (
            self.net
        ), "You need to load the model first. Please run load_model method."
        
        # fmt: off
        assert self.bounding_boxes is not None, "You need to inference the model first. Run predict func."
        assert self.scores is not None, "You need to inference the model first. Run predict func."
        assert self.class_IDs is not None, "You need to inference the model first. Run predict func."
        
        ax = utils.viz.plot_bbox(
            img,
            self.bounding_boxes[0],
            self.scores[0],
            self.class_IDs[0],
            class_names=self.net.classes,
        )
        
        plt.show()

    def get_model_options(self):
        """Get options for model name

        Returns:
            List[str]: model name options
        """
        options_for_yolo = []
        for model_name in model_zoo.get_model_list():
            if "yolo" in model_name.lower():
                options_for_yolo.append(model_name)
        return options_for_yolo
