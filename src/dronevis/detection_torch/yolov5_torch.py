import torch
import os
import getpass
import cv2
from dronevis.abstract import CVModel
import time
from dronevis.utils.image_process import write_fps
import numpy as np
from typing import Union


class YOLOv5(CVModel):
    """YOLOv5 implementation with torch hub model (inherits from CVModel).

    For more details see `YOLOv5 <https://pytorch.org/hub/ultralytics_yolov5>`_.
    """

    def __init__(self) -> None:
        """Initialize local path"""
        self.net = None
        self.model_local_path = f"/home/{getpass.getuser()}/.cache/torch/hub/ultralytics_yolov5_master"


    def load_model(self) -> None:
        """Load model from PyTorchHub"""
        print("Loading YOLOv5 Torch model ...")
        if os.path.exists(self.model_local_path):
            self.net = torch.hub.load(self.model_local_path, "yolov5s", source="local")
        else:
            self.net = torch.hub.load("ultralytics/yolov5", "yolov5s")

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Idle transformation.

        **Implemented just for code integrity**


        Args:
            image (np.ndarray): input image

        Returns:
            np.ndarray: output image
        """
        return image

    def predict(self, image: np.ndarray):
        """Run model inference on input image and return
        bouding boxes along with object names

        Args:
            image (np.array): input image

        Returns:
            torch.hub.models.self.common.Detections: detections object
        """
        assert (
            self.net
        ), "Please load the model first by invoking the ``load_model`` method."
        return self.net(image).render()[0]

    def detect_webcam(
        self,
        video_index: Union[str, int] = 0,
        window_name: str = "Cam Detection",
    ) -> None:
        """Start webcam detection from video_index
        *(to quit running this function press 'q')*

        The stream is retrieved and decoded using `opencv library <https://opencv.org/>`_.

        Args:
            video_index (Union[str, int], optional): index of video stream device. Defaults to 0 (webcam).
            window_name (str, optional): name of cv2 window. Defaults to "Cam Detection".
        """
        cap: cv2.VideoCapture = cv2.VideoCapture(video_index)
        prev_time = 0
        while True:
            _, frame = cap.read()

            image = self.predict(frame)
            cur_time = time.time()
            fps = 1 / (cur_time - prev_time)
            cv2.imshow(window_name, write_fps(image, fps))
            prev_time = cur_time
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()
        cap.release()
