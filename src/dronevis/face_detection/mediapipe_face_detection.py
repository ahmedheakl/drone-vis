import cv2
import mediapipe as mp
from dronevis.abstract import CVModel
from dronevis.utils.image_process import write_fps
import time
import numpy as np
from typing import Union


class FaceDetectModel(CVModel):
    """Face detection class with mediapipe

    This class inherits from base class ``CVModel``, and implements
    its abstract methods for code integrity.
    """

    def __init__(self, confidence: float = 0.6) -> None:
        """Construct model instance

        Args:
            confidence (float, optional): threshold for detection, **input is a probability [0, 1]**.
            Defaults to 0.5.
        """
        assert 0.0 <= confidence <= 1, "Confidence must be a score between 0 and 1"
        assert isinstance(confidence, (int, float)), "Confidence must be a number"
        self.face_detection = mp.solutions.face_detection.FaceDetection(confidence)
        self.mp_drawing = mp.solutions.drawing_utils

    def transform_img(self, img: np.ndarray) -> np.ndarray:
        """Tranform input image to be inference-ready
        Transformations is basically swapping ``BGR`` channels
        to ``RGB`` channels.

        Args:
            img (np.array): input image to be tranformed

        Returns:
            np.array: transformed image into ``RGB`` channels style
        """
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def load_model(self):
        """Load model *(no loading needed, all done in the constructor)*"""
        pass

    def predict(self, img: np.ndarray) -> np.ndarray:
        """Run model inference on input image and output face detection
        keypoints.

        Args:
            img (np.array): input image (assumed to be non-transformed)

        Returns:
            np.array: output image with keypoints drawn
        """
        image = self.transform_img(img)
        results = self.face_detection.process(image)
        if results.detections:
            for detection in results.detections:
                self.mp_drawing.draw_detection(img, detection)

        return img

    def detect_webcam(
        self,
        video_index: Union[int, str] = 0,
        window_name: str = "Face Detection",
    ) -> None:
        """Run webcam (or any video streaming device) with face detection module

        Args:
            video_index (Union[int, str], optional): index of video device. can be an ``IP`` or ``video_path``. Defaults to 0.
            window_name (str, optional): name of opencv window. Defaults to "Face Detection".
        """
        cap = cv2.VideoCapture(video_index)
        prev_time = 0
        while True:
            _, frame = cap.read()
            cur_time = time.time()
            image = self.predict(frame)
            fps = 1 / (cur_time - prev_time)
            cv2.imshow(window_name, write_fps(image, fps))
            prev_time = cur_time
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()
        cap.release()
