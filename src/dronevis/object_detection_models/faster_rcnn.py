import torch
import torchvision
import torchvision.transforms as transforms
from typing import List
import cv2
import numpy as np
from PIL import Image
from dronevis.config.config import COCO_NAMES

class FasterRCNN:
    def __init__(self) -> None:
        """Initialize faster R-CNN model"""

        # classes that the model may predict
        self.coco_names = COCO_NAMES
        
        self.COLORS = np.random.uniform(0, 255, size=(len(self.coco_names), 3))

        self.transform = transforms.Compose(
            [
                transforms.ToTensor(),
            ]
        )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.net = None

    def load_model(self, model_path=None):
        """Load model from PyTorchHub

        Args:
            model_path (str, optional): no need to use it, only for integrity with absract class. Defaults to None.
        """
        self.net = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn(
            pretrained=True
        )
        self.net = self.net.eval().to(self.device)

    def predict(self, image, detection_threshold: float = 0.7):
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
        with torch.no_grad():
            image = self.transform(image)
            image = image.unsqueeze(0)  # add a batch dimension
            outputs = self.net(image)[0]  # get outputs array
            pred_classes = [self.coco_names[i] for i in outputs["labels"].cpu().numpy()]
            pred_scores = outputs["scores"].detach().cpu().numpy()
            pred_bboxes = outputs["boxes"].detach().cpu().numpy()
            boxes = pred_bboxes[pred_scores >= detection_threshold].astype(np.int32)
        print(type(boxes), type(pred_classes), type(outputs["labels"]))
        return boxes, pred_classes, outputs["labels"]

    def transform_img(self, img):
        """Transform image to tensor

        Args:
            img (np.ndarray): input array

        Returns:
            torch.Tensor: tensor img
        """
        return self.transform(img).to(self.device)

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
                image,
                classes[i],
                (int(box[0]), int(box[1] - 5)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
                lineType=cv2.LINE_AA,
            )
        return image

    def detect_webcam(self) -> None:
        """Detecting objects with a webcam using FasterRCNN model
        (to quit running this function press 'q')"""

        cam_index = 0
        cap = cv2.VideoCapture(cam_index)
        if not cap.isOpened():
            print("Error while trying to read video. Please check path again")

        while cap.isOpened():
            _, frame = cap.read()

            boxes, classes, labels = self.predict(frame, 0.7)
            image = self.draw_boxes(boxes, classes, labels, frame)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imshow("image", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    def load_and_predict(self, img_path: str, output_path=None):
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


if __name__ == "__main__":
    model = FasterRCNN()
    model.load_model()
    model.detect_webcam()
