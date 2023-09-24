"""Inteface for drone classes"""
from typing import Callable, Optional
import logging
import socket

from dronevis.abstract.base_video_thread import BaseVideoThread
from dronevis.models import models_list

_LOG = logging.getLogger(__name__)


class BaseDrone:
    """Interface and base class for real and demo drone"""

    def __init__(self, ip_address: str = "192.168.1.1") -> None:
        if not self._validate_ip(ip_address):
            raise ValueError(f"Invalid IP address {ip_address}")

        self.ip_address = ip_address
        self.is_connected = False
        self.video_thread: Optional[BaseVideoThread] = None

    def _validate_ip(self, ip_address) -> bool:
        """Validate input IP address"""
        try:
            socket.inet_aton(ip_address)
            return True
        except OSError:
            return False

    def connect_video(
        self,
        close_callback: Callable,
        operation_callback: Callable,
        model_name: str,
    ) -> None:
        """Initialize and start video thread

        Args:
            close_callback (Callable): Callback to be invoked after closing the video thread
            model_name (str): Computer vision to run over the video stream
            operation_callback (Callable): Callback to be invoked after each operation

        Raises:
            TypeError: Provided callback should be callable
        """

        if not hasattr(close_callback, "__call__"):
            err_message = "Close callback provided is not callable"
            _LOG.critical(err_message)
            raise TypeError(err_message)

        if not hasattr(operation_callback, "__call__"):
            err_message = "Operation callback provided is not callable"
            _LOG.critical(err_message)
            raise TypeError(err_message)

        if model_name not in models_list:
            err_message = f"Model {model_name} is not supported"
            _LOG.critical(err_message)
            raise ValueError(err_message)

    def disconnect_video(self) -> None:
        """Disconnect video stream"""

    def connect(self) -> None:
        """Start communication thread to send control commands

        Raises:
            ConnectionError: Lost connection to drone
            ConnectionError: Cannot send commands to drone
        """

    def takeoff(self) -> bool:
        """Take Off"""
        return True

    def land(self) -> bool:
        """Land"""
        return True

    def calibrate(self) -> bool:
        """Calibrate"""
        return True

    def forward(self) -> bool:
        """Forward"""
        return True

    def backward(self) -> bool:
        """Backward"""
        return True

    def left(self) -> bool:
        """Left Move"""
        return True

    def right(self) -> bool:
        """Right Move"""
        return True

    def upward(self) -> bool:
        """Upward"""
        return True

    def downward(self) -> bool:
        """Downward"""
        return True

    def rotate_left(self) -> bool:
        """Rotate Left"""
        return True

    def rotate_right(self) -> bool:
        """Rotate Right"""
        return True

    def hover(self) -> bool:
        """Hover"""
        return True

    def emergency(self) -> bool:
        """Emergency"""
        return True

    def stop(self) -> None:
        """Stop Move"""

    def reset(self) -> bool:
        """Reset"""
        return True

    def set_config(self, **kwargs: bool) -> bool:
        """Setter for activating data retrival"""
        _ = kwargs
        return True

    def set_callback(self, callback: Callable) -> None:
        """Callback setter for navigation data handling"""
