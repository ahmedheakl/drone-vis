from abc import abstractmethod
from gluoncv import utils, model_zoo
from dronevis.abstract.abstract_model import CVModel
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
from dronevis.utils.image_process import write_fps

class GluonCVModel(CVModel):
    """Base class (inherits from CV abstract model) for creating custom gluoncv models.
    To use the abstract class just inherit it, and override the following abstract methods:
    
    - ``transform_img``: transform input image to be fed into model for inference
    - ``load_and_transform_img``: load image from given path and transform it
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
        """Show bounding boxes on input on ``matplotlib`` window
        
        .. note::
            
            You must run the inference in the input image first
            
        Args:
            img (np.array): input_image
        """
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
    def load_and_transform_img(self, img_path):
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
    
    def detect_webcam(self, video_index=0, window_name: str="Cam Detection") -> None:
        """Detecting objects with a webcam using current model
        *(to quit running this function press 'q')*

        Args:
            video_index (int | str, optional): index of cam, can be a `url`. Defaults to 0.
            window_name (str, optional): name of video window. Defaults to "Cam Detection".
        """

        cap = cv2.VideoCapture(video_index)
        if not cap.isOpened():
            print("Error while trying to read video. Please check path again")

        while cap.isOpened():
            _, frame = cap.read()
            start_time = time.time()
            x, img = self.transform_img(frame)
            image = self.predict(img, x)
            end_time = time.time()
            fps = 1 / (end_time - start_time)
            wait_time = max(1, int(fps / 4))
            cv2.imshow(window_name, write_fps(image, fps))
            if cv2.waitKey(wait_time) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
