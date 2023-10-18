"""Implementation for the DNN Face Detection model"""
from typing import List, Tuple, Optional
import logging
import time

import cv2
import numpy as np

from dronevis.abstract import CVModel
from dronevis.utils.general import download_file, write_fps
from dronevis.config.general import MODELS_URLS

_LOG = logging.getLogger(__name__)


class DNNFaceDetection(CVModel):
    """DNN Face Detection model"""

    size: Tuple[int, int] = (300, 300)
    mean: List[int] = [104, 117, 123]

    def __init__(self, confidence: float = 0.5) -> None:
        if not isinstance(confidence, float):
            _LOG.warning("Confidence must be a float. Setting to default value 0.5")
            confidence = 0.5

        if confidence < 0 or confidence > 1:
            _LOG.warning(
                "Confidence must be between 0 and 1. Setting to default value 0.5"
            )
            confidence = 0.5

        self.confidence = confidence
        self.net: Optional[cv2.dnn.Net] = None

    def load_model(self, model_name: str = "caffee") -> None:
        """Load model weights

        Args:
            model_name (str, optional): Whether load the tensorflow quantized
            version or the caffee version.
            Defaults to "caffee".
        """
        if model_name not in ["caffee", "tf"]:
            raise ValueError("Model name must be either 'caffee' or 'tf'")

        if model_name == "caffee":
            model_file = download_file(*MODELS_URLS["dnn_face_detection_caffee"])
            config_file = download_file(*MODELS_URLS["dnn_face_detection_protof"])
            self.net = cv2.dnn.readNetFromCaffe(config_file, model_file)

        else:
            model_file = download_file(*MODELS_URLS["dnn_face_detection_tf"])
            config_file = download_file(*MODELS_URLS["dnn_face_detection_tf_txt"])
            self.net = cv2.dnn.readNetFromTensorflow(model_file, config_file)

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Transform image to be compatible with the model

        Args:
            image (np.ndarray): Image to transform

        Returns:
            np.ndarray: Transformed image
        """
        return image

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Predict on image

        Args:
            image (np.ndarray): Image to predict on

        Returns:
            np.ndarray: Predicted image
        """
        if self.net is None:
            _LOG.warning("Model not loaded. Loading model weights...")
            self.load_model()
            assert self.net, "Model not loaded properly"

        transformed_image = self.transform_img(image)
        blob = cv2.dnn.blobFromImage(
            transformed_image,
            scalefactor=1.0,
            size=self.size,
            mean=self.mean,
            swapRB=False,
            crop=False,
        )

        self.net.setInput(blob)
        detections = self.net.forward()

        green_color = (0, 255, 0)
        thickness = 2

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                x1 = int(detections[0, 0, i, 3] * image.shape[1])
                y1 = int(detections[0, 0, i, 4] * image.shape[0])
                x2 = int(detections[0, 0, i, 5] * image.shape[1])
                y2 = int(detections[0, 0, i, 6] * image.shape[0])

                cv2.rectangle(image, (x1, y1), (x2, y2), green_color, thickness)

        return image

    def detect_webcam(
        self,
        video_index: Tuple[int, str] = 0,
        window_name="DNN Face Detection",
    ):
        cap = cv2.VideoCapture(video_index)

        if not cap.isOpened():
            _LOG.error("Cannot open camera")
            return

        while True:
            prev_time = time.perf_counter()
            ret, frame = cap.read()
            if not ret:
                _LOG.error("Can't receive frame. Exiting ...")
                break

            frame = self.predict(frame)
            fps = 1 / (time.perf_counter() - prev_time)
            cv2.imshow(window_name, write_fps(frame, fps))

            if cv2.waitKey(1) == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
