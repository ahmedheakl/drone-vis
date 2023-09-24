"""Implementation of video thread for drone stream retrieval"""
import threading
from typing import Callable

from dronevis.abstract.base_video_thread import BaseVideoThread


class VideoThread(BaseVideoThread):
    """Implementation of `BaseVideoInterface` for real drone"""

    video_port = 5555
    protocol = "tcp"

    def __init__(
        self,
        closing_callback: Callable,
        operation_callback: Callable,
        model_name: str,
        ip_address: str = "192.168.1.1",
    ) -> None:
        """Initialize drone instance

        Args:
            closing_callback (Callable): Callback to be invoked after closing thread
            operation_callback (Callable): Callback to be invoked after each operation
            model_name (str): Computer vision model to run inference on the video stream
            ip_address (str, optional): IP address of the drone. Defaults to "192.168.1.1".
        """
        video_index = f"{self.protocol}://{ip_address}:{self.video_port}"
        super().__init__(
            closing_callback,
            operation_callback,
            model_name,
            ip_address,
            video_index=video_index,
        )
        self.socket_lock = threading.Lock()
