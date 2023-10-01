"""Implementation of road segmentation and lane detection models"""
from typing import Optional
import time

import torch
import numpy as np
import cv2

from dronevis.abstract.abstract_model import CVModel
from dronevis.utils.general import device, write_fps


class YOLOP(CVModel):
    """YOLOP: You Only Look Once For Panoptic Driving Perception

    Paper: https://arxiv.org/abs/2108.11250
    """

    def __init__(self) -> None:
        """Initialize the model"""
        self.net: Optional[torch.nn.Module] = None
        self.size = 640

    def load_model(self, weights_name: str = "hustvl/yolop") -> None:
        """Load model weights from torch hub

        Args:
            weights_name (str, optional): Weights name on torch hub. Defaults to 'hustvl/yolop'.
        """
        self.net = torch.hub.load(weights_name, "yolop", pretrained=True)
        assert self.net, "Model not loaded properly"
        self.net.to(device=device())

    def transform_img(self, image: np.ndarray) -> torch.Tensor:
        """Run image transformation for YOLOP

        Args:
            image (np.ndarray): Source image

        Returns:
            torch.Tensor: Processed image
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (self.size, self.size))
        image_tensor: torch.Tensor = torch.from_numpy(image).to(device())
        image_tensor = image_tensor.permute(2, 0, 1).unsqueeze(0).float() / 255.0
        return image_tensor

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Predict the road segmentation of an image

        Args:
            image (torch.Tensor): Image to predict

        Returns:
            torch.Tensor: Road segmentation
        """
        return image

    def detect_webcam(self, video_index: int = 0, window_name="YOLOP"):
        """Detect road segmentation from webcam

        Args:
            video_index (int): Webcam index
            window_name (str, optional): Window name. Defaults to 'YOLOP'.
        """
        cap = cv2.VideoCapture(video_index)
        if not cap.isOpened():
            raise ValueError("Cannot open webcam")

        while True:
            prev_time = time.perf_counter()
            ret, frame = cap.read()
            if not ret:
                break

            frame = self.predict(frame)
            fps = 1 / (time.perf_counter() - prev_time)
            write_fps(frame, fps)
            cv2.imshow(window_name, frame)

            if cv2.waitKey(1) == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    def postprocess(self, image: torch.Tensor) -> np.ndarray:
        """Post process image after inference

        Args:
            image (torch.Tensor): Image to post process

        Returns:
            np.ndarray: Post processed image
        """
        image_arr = image.detach().cpu().squeeze(0).permute(1, 2, 0).numpy()
        return image_arr[:, :, 0]


class RoadSegmentation(YOLOP):
    """Implementation of road segmentation model"""

    def predict(self, image: np.ndarray, threshold: float = 0.7) -> np.ndarray:
        """Run inference for road segmentation

        Args:
            image (ndarray): Source image
            threshold (float, optional): Threshold for road segmentation. Defaults to 0.7.

        Returns:
            ndarray: Road segmentation
        """
        if self.net is None:
            self.load_model()
            assert self.net, "Model not loaded properly"

        color_overlay_increase = 80
        image_tensor = self.transform_img(image)
        _, segmentation, _ = self.net(image_tensor)
        pred_img = self.postprocess(segmentation)
        image = cv2.resize(image, (self.size, self.size))
        mask = pred_img < threshold
        image[:, :, 1][mask] += color_overlay_increase
        return image


class LaneDetection(YOLOP):
    """Implementation of lane detection model"""

    def predict(self, image: np.ndarray, threshold: float = 0.6) -> np.ndarray:
        """Run inference for lane detection

        Args:
            image (ndarray): Source image
            threshold (float, optional): Threshold for lane detection. Defaults to 0.6.

        Returns:
            ndarray: Lane detection
        """
        if self.net is None:
            self.load_model()
            assert self.net, "Model not loaded properly"

        image_tensor = self.transform_img(image)
        _, _, lane_detection = self.net(image_tensor)
        pred_img = self.postprocess(lane_detection)
        image = cv2.resize(image, (self.size, self.size))
        mask = pred_img < threshold
        image[:, :, 0][mask] = 0
        image[:, :, 1][mask] = 255
        image[:, :, 2][mask] = 0
        return image
