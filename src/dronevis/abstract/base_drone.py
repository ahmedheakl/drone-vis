"""Inteface for drone classes"""
from typing import Callable
import logging
from inspect import getmro

from dronevis.abstract import CVModel

_LOG = logging.getLogger(__name__)


class BaseDrone:
    """Interface and base class for real and demo drone"""

    def __init__(self, ip_address: str = "192.168.1.1") -> None:
        self.ip_address = ip_address

    def connect_video(self, callback: Callable, model: CVModel) -> None:
        """Initialize and start video thread

        Args:
            callback (Callable): Callback to be invoked after closing the video thread
            model (CVModel): Computer vision to run over the video stream

        Raises:
            TypeError: Provided callback should be callable
        """

        if not hasattr(callback, "__call__"):
            err_message = "Callback provided is not callable"
            _LOG.critical(err_message)
            raise TypeError(err_message)

        if CVModel not in getmro(type(model)):
            err_message = "Model provided is not an instance of ``CVModel``"
            _LOG.error(err_message)
            raise TypeError(err_message)

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

    def caliberate(self) -> bool:
        """Caliberate"""
        return True

    def foward(self) -> bool:
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

    def up(self) -> bool:
        """Upward"""
        return True

    def down(self) -> bool:
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
