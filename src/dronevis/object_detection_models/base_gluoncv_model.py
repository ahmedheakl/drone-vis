from abc import ABC, abstractmethod
from gluoncv import data, utils, model_zoo
from dronevis.object_detection_models.abstract_model import CVModel
import matplotlib.pyplot as plt
import numpy as np


class GluonCVModel(CVModel):
    """Base class for creating custom gluoncv models.
    To use the abstract class just inherit it, and override
    the abstract method.
    """
    
    def __init__(self, model_name: str, short_size: int=512) -> None:
        """Initialize Base model

        Args:
            model_name (str): name of the implemented model
            short_size (int, optional): Resize image short side to this short and keep aspect ratio.
                                        Defaults to 512.
        """
        self.short_size = short_size
        self.net = None
        self.class_IDs = None
        self.scores = None
        self.bounding_boxes = None
        self.model_name = model_name
        

    def load_model(self, model_path: str):
        """Load the model from model zoo.
        Run ``get_model_options`` to get model options.

        Args:
            model_name (str, optional): name of the pretrained model
        """
        self.net = model_zoo.get_model(model_path, pretrained=True)

    def predict(self, img, img_data=None):
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

    @abstractmethod
    def transform_img(self, img: np.ndarray):
        pass

    @abstractmethod
    def transform_and_load_img(self, img_path):
        pass

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

    def get_model_options(self):
        """Get options for model name
        
        Returns:
            List[str]: model name options
        """
        assert self.model_name is not None, "Use a model name."
        options_for_center_net = []
        for model_name in model_zoo.get_model_list():
            if self.model_name in model_name.lower():
                options_for_center_net.append(model_name)
        return options_for_center_net
