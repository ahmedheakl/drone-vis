"""Implementation of video thread for drone stream retrieval"""
import threading
from typing import Callable

from dronevis.abstract import CVModel
from dronevis.abstract.base_video_thread import BaseVideoThread


class VideoThread(BaseVideoThread):
    """Implementation of `BaseVideoInterface` for real drone"""

    video_port = 5555
    protocol = "tcp"

    def __init__(
        self,
        closing_callback: Callable,
        model: CVModel,
        ip_address: str = "192.168.1.1",
    ) -> None:
        """Initialize drone instance

        Args:
            closing_callback (Callable): Callback to be invoked after closing thread
            model (CVModel): Computer vision model to run inference on the video stream
            ip_address (str, optional): IP address of the drone. Defaults to "192.168.1.1".
        """
        super().__init__(closing_callback, model, ip_address)
        self.socket_lock = threading.Lock()
        self.video_index = f"{self.protocol}://{ip_address}:{self.video_port}"
