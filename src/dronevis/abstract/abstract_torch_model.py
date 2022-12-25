from abc import abstractmethod
from dronevis.abstract.abstract_model import CVModel
import numpy as np
import torch
from torchvision.transforms.functional import to_pil_image
import cv2
from typing import List
from PIL import Image
import time
from dronevis.config.config import COCO_NAMES
from dronevis.utils.image_process import write_fps
from typing import Union, Tuple


class TorchDetectionModel(CVModel):
    """Base class (inherits from CV abstract model) for creating custom PyTorch models.
    To use the abstract class just inherit it, and override the abstract method.
    """

    def __init__(self) -> None:
        """Construct torch models, and detect device for inference (cuda or cpu).

        Torch detection models are assumed to be trained on `COCO dataset <https://cocodataset.org/>`_.
        In addition, torch can detect if you have an available GPU. The property ``device``, contains the device
        that will be used for inference. You can change the device by changing the ``device`` property.
        """
        self.coco_names = COCO_NAMES

        self.COLORS = np.random.uniform(0, 255, size=(len(self.coco_names), 3))  # type: ignore
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.transform = None
        self.net = None

    @abstractmethod
    def load_model(self):
        pass

    def predict(
        self,
        input_image: np.ndarray,
        detection_threshold: float = 0.7,
    ) -> np.ndarray:
        """Predict all classes in an image using torch model

        Args:
            image (numpy.ndarray): video frame or image to predict the classes in it
            detection_threshold (float): thershold to determine if the calss will be taken or not

        Returns:
            numpy.ndarray: output image with boxes drawn
        """
        assert self.net, "Model not initialized! You need to load the model first. Please run `load_model`."
        assert detection_threshold >= 0.0 and detection_threshold <= 1.0, "Threshold must be a float between 0 and 1."
        assert self.transform, "Model not initialized. You need to load the model first. Please run `load_model`."

        image = input_image
        with torch.no_grad():
            image = self.transform_img(image).to(self.device)
            image = image.unsqueeze(0)  # add a batch dimension
            outputs = self.net(image)[0]  # get outputs array
            self.pred_classes = [self.coco_names[i] for i in outputs["labels"].cpu().numpy()]
            self.pred_scores = outputs["scores"].detach().cpu().numpy()
            self.pred_bboxes = outputs["boxes"].detach().cpu().numpy()
            self.boxes = self.pred_bboxes[self.pred_scores >= detection_threshold].astype(np.int32)

        image = self.draw_boxes(
            self.boxes,
            self.pred_classes,
            outputs["labels"],
            input_image,
        )
        return image

    def transform_img(self, img: np.ndarray) -> torch.Tensor:
        """Transform image to tensor

        Args:
            img (numpy.ndarray): input array

        Returns:
            torch.Tensor: tensor img
        """
        assert self.transform is not None, "Model not initialized. You need to load the model first. Please run `load_model`."
        return self.transform(to_pil_image(img)).to(self.device)

    def draw_boxes(
        self,
        boxes: np.ndarray,
        classes: List,
        labels: torch.Tensor,
        image: np.ndarray
    ) -> np.ndarray:
        """Draw boxes for the predicted classes in an image using torch model

        Args:
            boxes(numpy.ndarray): predicted boxes returned by predict function
            classes(List): predicted classes in an image returned by predict function
            labels(torch.Tensor): class labels in an image returned by predict function
            image(numpy.ndarray): an image to draw boxes on.

        Returns:
            numpy.ndarray: cv2 image after drawing boxes of the predicted classes on it with their labels
        """
        image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)
        for i, box in enumerate(boxes):
            color = self.COLORS[labels[i]]  # type: ignore
            cv2.rectangle(
                img=image,
                pt1=(int(box[0]), int(box[1])),
                pt2=(int(box[2]), int(box[3])),
                color=color,
                thickness=2
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
        return image

    def transform_and_load_img(self, img_path: str, output_path: str) -> None:
        """Detecting objects in a given image using torch model

        *(to quit running this function press 'q')*

        Args:
            img_path (str): path of the image to load
        """
        image = Image.open(img_path)
        image = np.asarray(image)
        boxes, classes, labels = self.predict(image)
        image = self.draw_boxes(boxes, classes, labels, image)
        cv2.imshow("Predicted Image", image)
        if output_path is not None:
            cv2.imwrite(output_path, image)
        cv2.waitKey(0)

    def detect_webcam(
        self,
        video_index: Union[int, str] = 0,
        window_name: str = "Cam Detection",
    ) -> None:
        """Detecting objects with a webcam using torch model
        *(to quit running this function press 'q')*

        The stream is retrieved and decoded using `opencv library <https://opencv.org/>`_.

        Args:
            video_index (int, optional): device index used to retrieve video stream, it can be an index or an IP. Defaults to 0.
            window_name (str, optional): name of video stream window. Defaults to "Cam Detection".
        """

        cap = cv2.VideoCapture(video_index)
        if not cap.isOpened():
            print("Error while trying to read video. Please check path again")
        prev_time = 0
        while cap.isOpened():
            _, frame = cap.read()
            with torch.no_grad():
                image = self.predict(frame, 0.7)
            cur_time = time.time()
            fps = 1 / (cur_time - prev_time)
            wait_time = max(1, int(fps / 4))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imshow(window_name, write_fps(image, fps))
            prev_time = cur_time
            if cv2.waitKey(wait_time) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    def frame_detection(self, frame: np.ndarray) -> Tuple[np.ndarray, float, float]:
        """Detect a single frame of a video stream

        Args:
            frame (numpy.ndarray): input frame

        Returns:
            Tuple[numpy.ndarray, float, fps]: image with detection results and wait time between frames
        """
        start_time = time.time()
        with torch.no_grad():
            image = self.predict(frame, 0.7)
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        wait_time = max(1, int(fps / 4))
        image = cv2.cvtColor(write_fps(image, fps), cv2.COLOR_BGR2RGB)
        return image, wait_time, fps
