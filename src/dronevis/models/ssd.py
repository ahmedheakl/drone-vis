from gluoncv import model_zoo, data, utils
from dronevis.models.abstract_model import CVModel
import mxnet as mx
import numpy as np


class SSD(CVModel):
    def __init__(self, short_size: int = 512) -> None:
        """Initialize SSD module

        Args:
            short_size (int, optional): Resize image short side to this short and keep aspect ratio.
                                        Defaults to 512.
        """
        self.short_size = short_size
        self.net = None
        self.class_IDs = None
        self.scores = None
        self.bounding_boxes = None

    def load_model(self, model_name: str = "ssd_512_mobilenet1.0_voc_int8") -> None:
        """Load the model from model zoo.
        options model = [
            ssd_512_mobilenet1.0_voc_int8,
            
            ssd_512_resnet50_v1_voc_int8, 
            ssd_512_resnet50_v1_voc,     
            
            ssd_300_vgg16_atrous_voc_int8,
            ssd_512_vgg16_atrous_voc_int8,
            
        ]
        Args:
            model_name (str, optional): name of the pretrained model
        """
        print("Loading SSD model")
        self.net = model_zoo.get_model(model_name, pretrained=True)

    def transform_img(self, img: np.ndarray):
        """Transform the input image to have a short side size of 512

        Args:
            img (np.ndarray): input image

        Returns:
            Tuple[mxnet.NDArray, np.ndarray]: A (1, 3, H, W) mxnet NDArray as input to network,
                                              and a numpy ndarray as original un-normalized color
                                              image for display
        """
        return data.transforms.presets.ssd.transform_test(
            mx.nd.array(img), short=self.short_size
        )

    def predict(self, img_data, img):
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
