"""Implementation for gesture recognition using mediapipe"""
# mypy: ignore-errors
from typing import Union, Optional, Tuple
import time
import copy
import itertools
from tkinter.ttk import Label

import cv2
import mediapipe as mp
import numpy as np
import torch
from torch import nn
from PIL import Image, ImageTk

from dronevis.abstract import CVModel
from dronevis.utils.general import write_fps, download_file, device
from dronevis.config.general import MODELS_URLS, GESTURES_LABELS


class GestureRecognition(CVModel):
    """Gesture Recognition class with mediapipe

    This class inherits from base class ``CVModel``, and implements
    its abstract methods for code integrity.
    """

    image_size: Tuple[int, int] = (250, 250)

    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        """Construct model instance

        Args:
            min_detection_confidence(float, optional): Threshold for detection
            min_tracking_confidence(float, optional): Threshold for tracking. Defaults to 0.5.
        """
        assert isinstance(
            min_detection_confidence, (int, float)
        ), "Confidence must be a number"

        assert isinstance(
            min_tracking_confidence, (int, float)
        ), "Confidence must be a number"
        assert (
            0.0 <= min_detection_confidence <= 1
        ), "Detection confidence must be a score between 0 and 1"
        assert isinstance(
            min_detection_confidence, (int, float)
        ), "Confidence must be a number"

        assert (
            0.0 <= min_tracking_confidence <= 1
        ), "Tracking confidence must be a score between 0 and 1"
        assert isinstance(
            min_tracking_confidence, (int, float)
        ), "Tracking must be a number"

        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands

        self.keypoints_classifier: Optional[nn.Module] = None
        self.hands: Optional[mp.solutions.hands.Hands] = None
        self.is_frame_detection = False

    def load_model(self, weights_path: Optional[str] = None) -> None:
        """Load model from memory"""
        if not weights_path:
            weights_path = download_file(*MODELS_URLS["gesture_recognition"])

        self.keypoints_classifier = KeypointsClassifier()
        self.keypoints_classifier = self.keypoints_classifier.to(device())
        self.keypoints_classifier.load_state_dict(torch.load(weights_path))
        self.keypoints_classifier.to(device=device())
        self.keypoints_classifier.double()

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Idle transformation of the image"""
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, self.image_size)
        return image

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Run model inference on input image and output gesture keypoints and name

        Args:
            img (np.array): Input image (assumed to be non-transformed)

        Returns:
            np.array: Output image with keypoints drawn and gesture label recognized
        """
        assert self.keypoints_classifier, "Please load the model first"
        image = self.transform_img(image)
        image.flags.writeable = False
        if not self.hands:
            self.hands = self.mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence,
            )

        results = self.hands.process(image)
        predicted_label = torch.tensor(-1)
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                debug_image = copy.deepcopy(image)
                landmark_list = self._calc_landmark_list(debug_image, hand_landmarks)
                pre_processed_landmark_list = self._pre_process_landmark(landmark_list)
                pre_processed_landmark_tensor = torch.tensor(
                    pre_processed_landmark_list,
                    dtype=torch.double,
                    device=device(),
                )

                output = self.keypoints_classifier(pre_processed_landmark_tensor)
                _, predicted_label = torch.max(output.unsqueeze(0), 1)
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style(),
                )

        image = cv2.flip(image, 1)

        if predicted_label.item() == -1:
            image = cv2.putText(
                img=image,
                text="No hand",
                org=(50, 50),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(255, 0, 0),
                thickness=1,
                lineType=cv2.LINE_AA,
            )

        else:

            def filter_func_(option: str) -> bool:
                return GESTURES_LABELS[option] == predicted_label.item()

            gesture_name = list(filter(filter_func_, GESTURES_LABELS))[0]
            image = cv2.putText(
                img=image,
                text=gesture_name,
                org=(50, 50),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(255, 0, 0),
                thickness=1,
                lineType=cv2.LINE_AA,
            )

        return image

    def detect_webcam(
        self,
        video_index: Union[int, str] = 0,
        window_name: str = "Gesture Recognition",
    ) -> None:
        """Run webcam (or any video streaming device) with gesture recognition module

        Args:
            video_index (Union[int, str], optional): Index of video device. can be an ``IP``
            or ``video_path``. Defaults to 0.
            window_name (str, optional): Name of opencv window. Defaults to "Gesture Recognition".
        """
        with self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        ) as self.hands:
            cap = cv2.VideoCapture(video_index)
            prev_time = 0.0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                cur_time = time.time()
                image = self.predict(frame)
                fps = 1 / (cur_time - prev_time)
                cv2.imshow(window_name, write_fps(image, fps))
                prev_time = cur_time
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        cv2.destroyAllWindows()
        cap.release()

    def on_frame_detect(self, label: Label, video_index: Union[int, str] = 0) -> None:
        """Run detection on tkinter label

        Args:
            label (Label): Tkinter label to view output
            video_index (int, optional): Index of the video device. Defaults to 0.
        """
        cap = cv2.VideoCapture(video_index)
        self.is_frame_detection = True

        def update_frame(label, cap):
            with self.mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence,
            ) as self.hands:
                ret, frame = cap.read()
                if ret is False:
                    return
                image = self.predict(frame)
                img = Image.fromarray(image)
                img = img.resize((400, 380), Image.BILINEAR)
                imgtk = ImageTk.PhotoImage(image=img)
                label.imgtk = imgtk
                label.configure(image=imgtk)
            if self.is_frame_detection:
                label.after(1, update_frame, label, cap)
            else:
                cap.release()

        update_frame(label, cap)

    def stop_frame_detection(self) -> None:
        """Stop frame detection"""
        self.is_frame_detection = False

    def _calc_landmark_list(
        self,
        image: np.ndarray,
        landmarks,
    ) -> list:
        """Calculate the landwarks in an image

        Args:
            image (np.array): Input image
            landmarks (dict): Dictonary of hand keypoints detected in an image.

        Returns:
            list: List of hand keypoints detected in an image
        """
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_point = []
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_z = landmark.z
            landmark_point.append([landmark_x, landmark_y, landmark_z])
        return landmark_point

    def _pre_process_landmark(self, landmark_list: list) -> list:
        """Converts calculated landmarks to relative coordinates and normalizes them

        Args:
            image (np.array): Input image
            landmark_list (dict): List of hand keypoints detected in an image.

        Returns:
            list: List of normalized hand keypoints after conversion to relative coordinates
        """
        temp_landmark_list = copy.deepcopy(landmark_list)
        base_x, base_y, base_z = 0, 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y, base_z = (
                    landmark_point[0],
                    landmark_point[1],
                    landmark_point[2],
                )

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
            temp_landmark_list[index][2] = temp_landmark_list[index][2] - base_z

        temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))
        temp_landmark_list = list(map(abs, temp_landmark_list))
        max_value = max(temp_landmark_list)

        def normalize_(value):
            return value / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list


class KeypointsClassifier(nn.Module):
    """Keypoints classifier model"""

    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(63, 50)
        torch.nn.init.xavier_uniform_(self.fc1.weight)
        self.leakyrelu = nn.LeakyReLU(inplace=True)
        self.fc2 = nn.Linear(50, 6)
        torch.nn.init.xavier_uniform_(self.fc2.weight)

    def forward(self, keypoints: torch.Tensor) -> torch.Tensor:
        """Forward pass through the keypoints classifier model"""
        output = self.fc1(keypoints)
        output = self.leakyrelu(output)
        output = self.fc2(output)
        return output
