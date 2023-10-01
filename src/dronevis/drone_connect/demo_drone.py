"""Implementation for demo drone for testing purposes"""
from typing import Optional, Callable, Union
import logging
import random
import time
from threading import Thread

from dronevis.abstract.base_drone import BaseDrone
from dronevis.abstract.base_video_thread import BaseVideoThread

_LOG = logging.getLogger(__name__)


class DemoDrone(BaseDrone):
    """Demo class for running ``demo GUI``."""

    def __init__(self, ip_address: str = "192.168.1.1") -> None:
        """Construct demo object"""
        super().__init__(ip_address)
        self.nav_thread: Optional[DemoNavThread] = None
        self.video_thread: Optional[DemoVideoThread] = None

    def connect_video(
        self,
        close_callback: Callable,
        operation_callback: Callable,
        model_name: str,
    ) -> None:
        """Retrieve video stream by connecting to the video port

        Args:
            close_callback (Callable): Callback after closing the video thread
            model_name (str): Computer vision model to run on the video stream
            operation_callback (Callable): Callback after each operation

        Raises:
            TypeError: `callback` must be a callable
            TypeError: The computer vision provided should implement the `CVModel`
            interface
        """

        super().connect_video(close_callback, operation_callback, model_name)

        self.video_thread = DemoVideoThread(
            close_callback,
            operation_callback,
            model_name,
        )
        self.video_thread.resume()

    def disconnect_video(self):
        """Disconnect video stream, and close the correspoding
        thread

        Raises:
            ValueError: Cannot close a stream that is not openned in the
            first place
        """
        if self.video_thread is None:
            err_message = "Video stream is not initialized"
            _LOG.error(err_message)
            raise ValueError(err_message)

        self.video_thread.stop()
        _LOG.debug("Video thread stopped")

    def connect(self) -> None:
        """Connect to drone
        Note that it is an idle method in this case
        """
        _LOG.info("drone connected")
        self.is_connected = True

    def set_callback(self, callback: Optional[Callable] = None) -> None:
        """Setter for callback

        Args:
            callback (Optional[Callable], optional): Callback function to be set. Defaults to None.

        Raises:
            TypeError: Provided callback should be a function or None.
        """
        if callback is None:
            callback = self._print_navdata

        if not hasattr(callback, "__call__"):
            err_message = "Please provide a function as a callback or None."
            _LOG.error(err_message)
            raise TypeError(err_message)

        if self.nav_thread is None:
            self.nav_thread = DemoNavThread(callback)
            self.nav_thread.start()
            _LOG.debug("Nav thread started")
        else:
            self.nav_thread.change_callback(callback)
            _LOG.debug("Changed callback")

    def set_config(self, **kwargs) -> bool:
        """Setter for configurations (gps, navdata)

        Args:
            activate_gps (bool, optional): Flag for starting gps. Defaults to True.
            activate_navdata (bool, optional): Flag for starting navdata. Defaults to True.
        """
        return True

    def _print_navdata(self, navdata: dict) -> None:
        """Trivial function for prining Navdata
        Should be used as a callback.

        Args:
            navdata (dict): Navigation data to be printed
        """
        print(navdata)

    def takeoff(self) -> bool:
        """Simulate taking off"""
        _LOG.info("Takeoff")
        return True

    def land(self) -> bool:
        """Simulate landing"""
        _LOG.info("Land")
        return True

    def calibrate(self) -> bool:
        """Simulate caliberation"""
        _LOG.info("Calibrate")
        return True

    def forward(self) -> bool:
        """Simulate forward movement"""
        _LOG.info("Forward")
        return True

    def backward(self) -> bool:
        """Simulate backward movement"""
        _LOG.info("Backward")
        return True

    def left(self) -> bool:
        """Simulate left movement"""
        _LOG.info("Left")
        return True

    def right(self) -> bool:
        """Simulate right movement"""
        _LOG.info("Right")
        return True

    def upward(self) -> bool:
        """Simulate up movement"""
        _LOG.info("Up")
        return True

    def downward(self) -> bool:
        """Simulate down movement"""
        _LOG.info("Down")
        return True

    def rotate_left(self) -> bool:
        """Simulate left rotation"""
        _LOG.info("Rotating left")
        return True

    def rotate_right(self) -> bool:
        """Simulate right rotation"""
        _LOG.info("Rotating right")
        return True

    def hover(self) -> bool:
        """Simulate hover movement"""
        _LOG.info("Hover")
        return True

    def emergency(self) -> bool:
        """Simulate emergency"""
        _LOG.info("Emergency")
        return True

    def stop(self) -> None:
        """Simulate stopping"""
        self.is_connected = False
        if self.video_thread is not None:
            self.video_thread.close_thread()
            self.video_thread.join()
            _LOG.debug("Video thread stopped")
            self.video_thread = None

        if self.nav_thread is not None:
            self.nav_thread.stop()
            self.nav_thread.join()
            _LOG.debug("Nav thread stopped")
            self.nav_thread = None

        _LOG.warning("Drone disconnected")

    def reset(self) -> bool:
        """Simulate resting"""
        _LOG.info("Reseting")
        return True


class DemoVideoThread(BaseVideoThread):
    """Demo for video thread implementing `BaseVideoThread` interface"""

    def __init__(
        self,
        closing_callback: Callable,
        operation_callback: Callable,
        model_name: str,
        ip_address: str = "192.168.1.1",
        video_index: Union[int, str] = 0,
    ) -> None:
        super().__init__(
            closing_callback,
            operation_callback,
            model_name,
            ip_address,
            video_index,
        )
        self.frame = "Demo Video Capture"


class DemoNavThread(Thread):
    """Demo for navigation data thread"""

    def __init__(
        self,
        callback: Callable,
    ):
        super().__init__()
        self.callback = callback
        self.running = True

    def change_callback(self, new_callback: Callable):
        """Setter for changing/setting callback for handling navdata

        Args:
            new_callback (Callable): New callback to be set

        Raises:
            TypeError: Callback provided should be a callable
        """

        if not hasattr(new_callback, "__call__"):
            err_message = "Please provide a function for callback"
            _LOG.error(err_message)
            raise TypeError(err_message)

        self.callback = new_callback

        _LOG.debug("Nav thread callback changed")

    def run(self):
        """Run navigation data thread"""
        velocity_x, velocity_y, velocity_z, height = [0.0] * 4
        battery = random.randint(0, 100)
        while self.running:
            velocity_x = self.moving_averge(velocity_x, random.uniform(0, 2000))
            velocity_y = self.moving_averge(velocity_y, random.uniform(0, 2000))
            velocity_z = self.moving_averge(velocity_z, random.uniform(0, 2000))
            height = self.moving_averge(height, random.uniform(0, 50000))

            data = {
                "navdata_demo": {
                    "battery_percentage": battery,
                    "vx": velocity_x,
                    "vy": velocity_y,
                    "vz": velocity_z,
                    "altitude": height,
                },
            }
            self.callback(data)
            time.sleep(0.05)

        _LOG.debug("closing nav thread ...")

    def moving_averge(self, old_value: float, new_value: float) -> float:
        """Get the next value for a moving average

        Args:
            old_value (float): Old consistent value
            new_value (float): New reading

        Returns:
            float: Next value in the graph
        """
        next_value: float = old_value * 0.9 + new_value * 0.1
        return next_value

    def stop(self):
        """Stop the running thread"""
        self.running = False
