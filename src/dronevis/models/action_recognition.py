"""Implementation of VideoMAE for video classification."""
from typing import Optional, Union, List
import logging

import torch
import numpy as np
from transformers import (
    AutoImageProcessor,
    VideoMAEForVideoClassification,
    TimesformerForVideoClassification,
    VivitModel,
    VivitImageProcessor,
)
import cv2

from dronevis.abstract import CVModel
from dronevis.utils.general import device

_LOG = logging.getLogger(__name__)


class ActionRecognizer(CVModel):
    """Action recognition class with VideoMAE

    This class inherits from base class ``CVModel``, and implements
    its abstract methods for code integrity.
    """

    ACTION_GOOGLE_WEGIHTS = "google/vivit-b-16x2-kinetics400"
    ACTION_FACEBOOK_WEIGHTS = "facebook/timesformer-base-finetuned-k600"
    ACTION_MCG_WEIGHTS = "MCG-NJU/videomae-base-finetuned-kinetics"

    def __init__(self, num_preds: int = 1) -> None:
        """Construct model instance

        Args:
            num_preds (int, optional): number of predictions to return.
            Defaults to 1.
        """
        self.num_preds = num_preds
        self.net: Optional[VideoMAEForVideoClassification] = None
        self.image_processor: Optional[AutoImageProcessor] = None

    def load_model(self, model_name: str = "mcg") -> None:
        """Load model from memory

        Args:
            model_name (str, optional): Type of the model to be used. There are
            3 available types ["google", "mcg", "facebook"]. Defaults to "mcg".
        """
        model_name = model_name.lower()
        if model_name == "google":
            self.image_processor = VivitImageProcessor.from_pretrained(
                self.ACTION_GOOGLE_WEGIHTS
            )
            self.net = VivitModel.from_pretrained(self.ACTION_GOOGLE_WEGIHTS)
        elif model_name == "mcg":
            self.image_processor = AutoImageProcessor.from_pretrained(
                self.ACTION_MCG_WEIGHTS
            )
            self.net = VideoMAEForVideoClassification.from_pretrained(
                self.ACTION_MCG_WEIGHTS
            )
        elif model_name == "facebook":
            self.image_processor = AutoImageProcessor.from_pretrained(
                self.ACTION_FACEBOOK_WEIGHTS
            )
            self.net = TimesformerForVideoClassification.from_pretrained(
                self.ACTION_FACEBOOK_WEIGHTS
            )
        else:
            raise ValueError(
                "Invalid model name. Please choose from [google, mcg, facebook]"
            )
        self.net.to(device())

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Transform input video

        Args:
            image (np.ndarray): input video, using "image" just for
            inheritance purpose
        """
        video = image
        if self.image_processor is None:
            _LOG.error("Model not loaded")
            return video

        video_tensor = self.image_processor(list(video), return_tensors="pt")
        video_tensor.to(device())
        return video_tensor

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Run model inference on the provided video

        Args:
            image (np.ndarray): input video, using "image" just for
            inheritance purpose

        Returns:
            List[str]: List of predicted labels
        """
        video = image
        if self.net is None:
            self.load_model()
            assert self.net

        video_tensor = self.transform_img(video)
        with torch.no_grad():
            outputs = self.net(**video_tensor)
            logits = outputs.logits

        predicted_labels = logits.argmax(-1).tolist()
        predicted_labels = np.array(
            [self.net.config.id2label[label] for label in predicted_labels]
        )
        return predicted_labels

    def detect_webcam(
        self,
        video_index: Union[int, str] = 0,
        window_name: str = "Action Recognition",
        num_frames: int = 16,
    ) -> None:
        """Run model inference on webcam feed

        Args:
            video (Union[int, str], optional): webcam id or video path.
            Defaults to 0.
            fps (int, optional): frames per second. Defaults to 30.
            window_name (str, optional): window name. Defaults to "Action Recognition".
            num_frames (int, optional): number of frames to sample. Defaults to 16.
        """
        cap = cv2.VideoCapture(video_index)
        counter = 0
        frames: List[np.ndarray] = []
        results: np.ndarray = np.array(["None"])
        while True:
            _, frame = cap.read()

            if frame is not None and counter > 0 and counter % num_frames == 0:
                video = np.stack(frames)
                results = self.predict(video)
                counter = 0
                frames = []

            if frame is None:
                _LOG.warning("No frame received")
                break
            frames += [frame[:, :, :]]
            counter += 1
            cv2.putText(
                frame,
                ", ".join(list(results)),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (100, 200, 0),
                2,
                cv2.LINE_AA,
            )
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
