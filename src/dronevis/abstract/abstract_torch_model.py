"""Interface for models implemented with PyTorch"""
from typing import Union, List, Optional
import time
import logging

import numpy as np
import torch
import torchvision
from torchvision.transforms.functional import to_pil_image
import cv2

from dronevis.config.general import COCO_NAMES
from dronevis.abstract.abstract_model import CVModel
from dronevis.utils.general import write_fps

_LOG = logging.getLogger(__name__)


class TorchDetectionModel(CVModel):
    """Base class (inherits from CV abstract model) for creating custom PyTorch models.
    To use the abstract class just inherit it, and override the abstract method.

    For each prediction, the model output 300 labels, and their corresponding 300 scores.
    Labels are picked if they surpass the threshold accuracy.
    """

    coco_names = COCO_NAMES
    colors = np.random.uniform(0, 255, size=(len(COCO_NAMES), 3))

    def __init__(self) -> None:
        """Construct torch models, and detect device for inference (cuda or cpu).

        Torch detection models are assumed to be trained on
        `COCO dataset <https://cocodataset.org/>`_. In addition, torch can detect if
        you have an available GPU. The property ``device``, contains the device that
        will be used for inference. You can change the device by changing the ``device`` property.
        """

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.transform: Optional[torchvision.transforms.Compose] = None
        self.net: Optional[torch.nn.Module] = None
        self.pred_classes: Optional[List[str]] = None
        self.pred_scores: Optional[np.ndarray] = None
        self.boxes: Optional[np.ndarray] = None

    def predict(
        self,
        image: np.ndarray,
        detection_threshold: float = 0.7,
    ) -> np.ndarray:
        """Predict all classes in an image using torch model

        Args:
            image (numpy.ndarray): video frame or image to predict the classes in it
            detection_threshold (float): thershold to determine if the calss will be taken or not

        Returns:
            numpy.ndarray: output image with boxes drawn
        """
        assert (
            self.net
        ), "Model not initialized! You need to load the model first. Please run `load_model`."
        assert (
            0.0 <= detection_threshold <= 1.0
        ), "Threshold must be a float between 0 and 1."

        input_image = image
        with torch.no_grad():
            transformed_image = self.transform_img(image).to(self.device)
            transformed_image = transformed_image.unsqueeze(0)  # add a batch dimension
            outputs = self.net(transformed_image)[0]  # get outputs array
            self.pred_classes = [
                self.coco_names[i] for i in outputs["labels"].cpu().numpy()
            ]
            pred_scores = outputs["scores"].detach().cpu().numpy()
            pred_bboxes = outputs["boxes"].detach().cpu().numpy()
            boxes = pred_bboxes[pred_scores >= detection_threshold].astype(np.int32)

        drawn_image = self.draw_boxes(
            boxes,
            self.pred_classes,
            outputs["labels"],
            input_image,
        )
        self.boxes = boxes
        self.pred_scores = pred_scores
        return drawn_image

    def transform_img(self, image: np.ndarray) -> torch.Tensor:
        """Transform image to tensor

        Args:
            img (numpy.ndarray): input array

        Returns:
            torch.Tensor: tensor img
        """
        assert (
            self.transform is not None
        ), "Model not initialized. You need to load the model first. Please run `load_model`."
        pil_image = to_pil_image(image)
        transformed_image = self.transform(pil_image).to(self.device)
        return transformed_image

    def draw_boxes(
        self,
        boxes: np.ndarray,
        classes: List[str],
        labels: torch.Tensor,
        image: np.ndarray,
    ) -> np.ndarray:
        """Draw boxes for the predicted classes in an image using torch model

        Args:
            boxes(numpy.ndarray): predicted boxes returned by predict function
            classes(List): predicted classes in an image returned by predict function
            labels(torch.Tensor): class labels in an image returned by predict function
            image(numpy.ndarray): an image to draw boxes on.

        Returns:
            numpy.ndarray: cv2 image after drawing boxes of the predicted classes on
            it with their labels
        """
        image = cv2.cvtColor(np.asarray(image, dtype=np.float32), cv2.COLOR_BGR2RGB)
        for i, box in enumerate(boxes):
            color = self.colors[labels[i]]
            cv2.rectangle(
                img=image,
                pt1=(int(box[0]), int(box[1])),
                pt2=(int(box[2]), int(box[3])),
                color=color,
                thickness=2,
            )
            cv2.putText(
                img=image,
                text=classes[i],
                org=(int(box[0]), int(box[1] - 5)),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.8,
                color=color,
                thickness=2,
                lineType=cv2.LINE_AA,
            )
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def detect_webcam(
        self,
        video_index: Union[int, str] = 0,
        window_name: str = "Cam Detection",
    ) -> None:
        """Detecting objects with a webcam using torch model
        *(to quit running this function press 'q')*

        The stream is retrieved and decoded using `opencv library <https://opencv.org/>`_.

        Args:
            video_index (int, optional): device index used to retrieve video stream, it
            can be an index or an IP. Defaults to 0.
            window_name (str, optional): name of video stream window. Defaults to "Cam Detection".
        """

        cap = cv2.VideoCapture(video_index)

        while cap.isOpened():
            prev_time = time.time()
            _, frame = cap.read()
            with torch.no_grad():
                image = self.predict(frame, 0.7)
            fps = 1 / (time.time() - prev_time)
            wait_time = max(1, int(fps / 4))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imshow(window_name, write_fps(image, fps))
            if cv2.waitKey(wait_time) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
