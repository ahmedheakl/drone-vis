"""Interface for video thread"""
import threading
from typing import Callable, Union
import logging
import time
import cv2

from dronevis.abstract.abstract_model import CVModel
from dronevis.utils.general import write_fps

_LOG = logging.getLogger(__name__)


class BaseVideoThread(threading.Thread):
    """Abstract class for the video used in both `Drone` and `DemoDrone`"""

    def __init__(
        self,
        closing_callback: Callable,
        model: CVModel,
        ip_address: str = "192.168.1.1",
    ):
        super().__init__()
        self.close_callback = closing_callback
        self.ip_address = ip_address
        self.model = model
        self.running = True
        self.video_index: Union[str, int] = 0
        self.frame_name = "Video Capture"

    def run(self) -> None:
        """Create video stream and view frames"""

        cap = cv2.VideoCapture(self.video_index)
        if not cap.isOpened():
            _LOG.warning("Error while trying to read video. Please check path again")

        prev_time = 0.0
        while cap.isOpened():
            if not self.running:
                break

            _, frame = cap.read()
            frame = self.model.predict(frame)
            cur_time = time.time()
            fps = 1 / (cur_time - prev_time)
            prev_time = cur_time
            cv2.imshow(self.frame_name, write_fps(frame, fps))

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        _LOG.info("Closing video stream ...")
        cap.release()
        cv2.destroyAllWindows()
        self.close_callback()
        _LOG.info("Closed video stream")

    def change_model(self, model: CVModel):
        """Change computer vision model running on the video stream"""
        self.model = model
        _LOG.debug("Model for video thread changed")

    def stop(self) -> None:
        """Stop the running video thread"""
        self.running = False
