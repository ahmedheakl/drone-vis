from abc import abstractmethod
from dronevis.object_detection_models.abstract_model import CVModel
import numpy as np
import torch
from torchvision.transforms.functional import to_pil_image
import cv2
from typing import List
from PIL import Image
import time
from dronevis.config.config import COCO_NAMES



class TorchDetectionModel(CVModel):
    """Base class for creating custom PyTorch models.
    To use the abstract class just inherit it, and override
    the abstract method.
    """    
    def __init__(self) -> None:
        self.coco_names = COCO_NAMES

        self.COLORS = np.random.uniform(0, 255, size=(len(self.coco_names), 3))

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net = None    
    @abstractmethod
    def load_model(self):
        pass

    def predict(self, image, detection_threshold=0.7):
        """Predict all classes in an image using FasterRCNN model
        Args:
            image(np.ndarray): video frame or image to predict the classes in it.
            detection_threshold(float): thershold to determine if the calss will be taken or not.

        Returns:
            np.ndarray: boxes surrounding predicted classes (above the given detection_threshold)
            List: predicted classes list
            torch.Tensor: labels of the predicted classes

        """
        assert self.net, "You need to load the model first. Please run `load_model`."
        input_image = image
        with torch.no_grad():
            image = to_pil_image(image)
            image = self.transform(image)
            image = image.unsqueeze(0)  # add a batch dimension
            outputs = self.net(image)[0]  # get outputs array
            pred_classes = [self.coco_names[i] for i in outputs["labels"].cpu().numpy()]
            pred_scores = outputs["scores"].detach().cpu().numpy()
            pred_bboxes = outputs["boxes"].detach().cpu().numpy()
            boxes = pred_bboxes[pred_scores >= detection_threshold].astype(np.int32)
            
        image = self.draw_boxes(boxes, pred_classes, outputs["labels"], input_image)
        return boxes, pred_classes, outputs["labels"], image


    def transform_img(self, img: np.ndarray):
        """Transform image to tensor

        Args:
            img (np.ndarray): input array

        Returns:
            torch.Tensor: tensor img
        """
        return self.transform(to_pil_image(img)).to(self.device)
    
    def draw_boxes(self, boxes: np.ndarray, classes: List, labels: torch.Tensor, image):
        """Draw boxes for the predicted classes in an image using FasterRCNN model

        Args:
            boxes(np.ndarray): predicted boxes returned by predict function
            classes(List): predicted classes in an image returned by predict function
            labels(torch.Tensor): class labels in an image returned by predict function
            image(np.ndarray): an image to draw boxes on.

        Returns:
            np.ndarray: cv2 image after drawing boxes of the predicted classes on it with their labels
        """
        image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)
        for i, box in enumerate(boxes):
            color = self.COLORS[labels[i]]  # type: ignore
            cv2.rectangle(
                image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 2
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
    
    
    def transform_and_load_img(self, img_path, output_path):
        """Detecting objects in a given image using FasterRCNN model
            (to quit running this function press 'q')

        Args:
            img_path (str): path of the image to load
        """
        image = Image.open(img_path)
        boxes, classes, labels = self.predict(image)
        image = self.draw_boxes(boxes, classes, labels, image)
        cv2.imshow("Predicted Image", image)
        if output_path is not None:
            cv2.imwrite(output_path, image)
        cv2.waitKey(0)
        
    def detect_webcam(self, video_index=0) -> None:
        """Detecting objects with a webcam using FasterRCNN model
        (to quit running this function press 'q')"""

        cap = cv2.VideoCapture(video_index)
        if not cap.isOpened():
            print("Error while trying to read video. Please check path again")

        while cap.isOpened():
            _, frame = cap.read()
            start_time = time.time()
            with torch.no_grad():
                _, _, _, image = self.predict(frame, 0.7)
            end_time = time.time()
            fps = 1 / (end_time - start_time)
            cv2.putText(
                image,
                f"{fps:.3f} FPS",
                (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            wait_time = max(1, int(fps / 4))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imshow("image", image)
            if cv2.waitKey(wait_time) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

