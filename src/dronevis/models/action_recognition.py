"""Implementation of VideoMAE for video classification."""
from typing import Optional, Union, List
import logging
import time

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
from dronevis.utils.general import device, write_fps

_LOG = logging.getLogger(__name__)


class ActionRecognizer(CVModel):
    """Action recognition class with VideoMAE

    This class inherits from base class ``CVModel``, and implements
    its abstract methods for code integrity.
    """

    def __init__(self, num_preds: int = 1) -> None:
        """Construct model instance

        Args:
            num_preds (int, optional): number of predictions to return.
            Defaults to 1.
        """
        self.num_preds = num_preds
        self.model: Optional[VideoMAEForVideoClassification] = None
        self.image_processor: Optional[AutoImageProcessor] = None

    def load_model(
        self,
        weights: str = "MCG-NJU/videomae-base-finetuned-kinetics",
    ) -> None:
        """Load model from memory

        Args:
            weights (str, optional): Weights name to be downloaded from huggingface.
            Defaults to "MCG-NJU/videomae-base-finetuned-kinetics".
        """
        # self.model = VideoMAEForVideoClassification.from_pretrained(weights)

        # self.image_processor = AutoImageProcessor.from_pretrained(weights)
        # self.image_processor = AutoImageProcessor.from_pretrained(
        #     "facebook/timesformer-base-finetuned-k600"
        # )
        # self.model = TimesformerForVideoClassification.from_pretrained(
        #     "facebook/timesformer-base-finetuned-k600"
        # )

        self.image_processor = VivitImageProcessor.from_pretrained(
            "google/vivit-b-16x2-kinetics400"
        )
        self.model = VivitModel.from_pretrained("google/vivit-b-16x2-kinetics400")
        self.model.to(device())

    def transform_img(self, video: np.ndarray) -> np.ndarray:
        """Transform input video

        Args:
            video (np.ndarray): input video
        """
        if self.image_processor is None:
            _LOG.error("Model not loaded")
            return video

        video_tensor = self.image_processor(list(video), return_tensors="pt")
        video_tensor.to(device())
        return video_tensor

    def predict(self, video: np.ndarray) -> List[str]:
        """Run model inference on the provided video

        Args:
            video (np.ndarray): input video

        Returns:
            List[str]: List of predicted labels
        """
        if self.model is None:
            _LOG.error("Model not loaded")
            return []

        video_tensor = self.transform_img(video)
        with torch.no_grad():
            outputs = self.model(**video_tensor)
            logits = outputs.logits

        predicted_labels = logits.argmax(-1).tolist()
        predicted_labels = [
            self.model.config.id2label[label] for label in predicted_labels
        ]
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
        results: List[str] = ["None"]
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
                ", ".join(results),
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
