"""Implementation for gesture recognition using mediapipe"""
from typing import Union
import time
import cv2
import mediapipe as mp
import numpy as np
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import *
import itertools
import copy
import os
from os.path import isfile, join

from dronevis.abstract import CVModel
from dronevis.utils.general import write_fps

Keypoint_classifier_model_path = join(os.getcwd(),r'src\dronevis\models\hand_keypoint_model_weights.pth')
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
gesture_labels_dict = {"Down":0,"Forward":1, "Left":2, "Right":3, "Stop":4, "Up":5}

class GestureRecognition(CVModel):
    """Gesture Recognition class with mediapipe

    This class inherits from base class ``CVModel``, and implements
    its abstract methods for code integrity.
    """

    def __init__(self, min_detection_confidence: float = 0.5, min_tracking_confidence: float=0.5) -> None:
        """Construct model instance

        Args:
            min_detection_confidence(float, optional): threshold for detection
            min_tracking_confidence(float, optional): threshold for tracking,
            **input is a probability [0, 1]**.
            Defaults to 0.5.
        """
        assert 0.0 <= min_detection_confidence <= 1, "Detection confidence must be a score between 0 and 1"
        assert isinstance(min_detection_confidence, (int, float)), "Confidence must be a number"
        
        assert 0.0 <= min_tracking_confidence <= 1, "Tracking confidence must be a score between 0 and 1"
        assert isinstance(min_tracking_confidence, (int, float)), "Tracking must be a number"

        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mp_drawing = mp.solutions.drawing_utils # type: ignore
        self.mp_drawing_styles = mp.solutions.drawing_styles  # type: ignore
        self.mp_hands = mp.solutions.hands  # type: ignore
    
    def load_model(self) -> None:
        """Load model from memory"""
        self.keypoints_classifier_model = Keypoint_classifier()
        self.keypoints_classifier_model = self.keypoints_classifier_model.to(device)
        self.keypoints_classifier_model.load_state_dict(torch.load(Keypoint_classifier_model_path))
        self.keypoints_classifier_model.double()

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Idle transformation of the image"""
        return image
    
    
    def predict(self, image: np.ndarray) -> np.ndarray:
        """Run model inference on input image and output gesture keypoints and name

        Args:
            img (np.array): input image (assumed to be non-transformed)

        Returns:
            np.array: output image with keypoints drawn and gesture label recognized
        """
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        predicted_label = -1
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                debug_image = copy.deepcopy(image)
                landmark_list = self.__calc_landmark_list(debug_image, hand_landmarks)
                pre_processed_landmark_list = self.__pre_process_landmark(landmark_list)
                output = self.keypoints_classifier_model(torch.tensor(pre_processed_landmark_list,dtype=torch.double))
                _, predicted_label = torch.max(output.unsqueeze(0),1)
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
        
        image = cv2.flip(image, 1)

        if predicted_label == -1:
            image = cv2.putText(img=image, text="No hand", org=(50, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale=1, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)

        else:
            gesture_name = list(filter(lambda x: gesture_labels_dict[x] == predicted_label.item(), gesture_labels_dict))[0]
            image = cv2.putText(img=image, text=gesture_name, org=(50, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale=1, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)

        return image

    def detect_webcam(
        self,
        video_index: Union[int, str] = 0,
        window_name: str = "Gesture Recognition",
    ) -> None:
        """Run webcam (or any video streaming device) with gesture recognition module

        Args:
            video_index (Union[int, str], optional): index of video device. can be an ``IP``
            or ``video_path``. Defaults to 0.
            window_name (str, optional): name of opencv window. Defaults to "Gesture Recognition".
        """
        with self.mp_hands.Hands(model_complexity=0,min_detection_confidence=self.min_detection_confidence,min_tracking_confidence=self.min_tracking_confidence) as self.hands:
            cap = cv2.VideoCapture(video_index)
            prev_time = 0.0
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


    def __calc_landmark_list(self,image: np.ndarray, landmarks:dict)-> list:
        """calculate the landwarks in an image

        Args:
            image (np.array): input image 
            landmarks (dict): dictonary of hand keypoints detected in an image.

        Returns:
            list: list of hand keypoints detected in an image
        """
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_point = []
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_z = landmark.z
            landmark_point.append([landmark_x, landmark_y,landmark_z])
        return landmark_point

    def __pre_process_landmark(self,landmark_list:list)->list:
        """converts calculated landmarks to relative coordinates and normalizes them

        Args:
            image (np.array): input image 
            landmark_list (dict): list of hand keypoints detected in an image.

        Returns:
            list: list of normalized hand keypoints after conversion to relative coordinates
        """
        temp_landmark_list = copy.deepcopy(landmark_list)
        base_x, base_y, base_z = 0, 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y, base_z = landmark_point[0], landmark_point[1], landmark_point[2]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
            temp_landmark_list[index][2] = temp_landmark_list[index][2] - base_z
        
        temp_landmark_list = list(
            itertools.chain.from_iterable(temp_landmark_list))

        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list
    


class Keypoint_classifier(nn.Module):
    def __init__(self):
        super(Keypoint_classifier, self).__init__()
        self.fc1 =  nn.Linear(63, 50)
        torch.nn.init.xavier_uniform_(self.fc1.weight)
        self.leakyrelu = nn.LeakyReLU(inplace=True)
        self.fc2 =  nn.Linear(50, 6)
        torch.nn.init.xavier_uniform_(self.fc2.weight)
              
    def forward(self, x):
        output = self.fc1(x)
        output = self.leakyrelu(output)
        output = self.fc2(output)
        return output