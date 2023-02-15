"""Implementation for demo drone for testing purposes"""
from typing import Optional, Union, Callable
import logging
import random
import time
from threading import Thread
from inspect import getmro
import cv2

from dronevis.utils.utils import write_fps
from dronevis.abstract import CVModel

_LOG = logging.getLogger(__name__)


class DemoDrone:
    """Demo class for running ``demo GUI``."""

    def __init__(
        self,
        ip_address: str = "192.168.1.1",
    ) -> None:
        """Construct demo object"""

        self.is_connected = False
        self.nav_thread: Optional[DemoNavThread] = None
        self.video_thread: Optional[DemoVideoThread] = None
        self.ip_address = ip_address

    def connect_video(self, callback: Callable, model: CVModel) -> None:
        """Retrieve video stream by connecting to the video port

        Args:
            callback (Callable): Callback after closing the video thread
            model (CVModel): Computer vision model to run on the video stream

        Raises:
            TypeError: `callback` must be a callable
            TypeError: The computer vision provided should implement the `CVModel`
            interface
        """

        if not hasattr(callable, "__call__"):
            err_message = "Please provide a function as a callback"
            _LOG.error(err_message)
            raise TypeError(err_message)

        if CVModel not in getmro(type(model)):
            err_message = "Model provided is not an instance of ``CVModel``"
            _LOG.error(err_message)
            raise TypeError(err_message)

        self.video_thread = DemoVideoThread(callback, model)
        self.video_thread.start()

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
        time.sleep(0.2)
        self.video_thread = None
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
            callback = self.print_navdata

        if not hasattr(callable, "__call__"):
            err_message = "Please provide a function as a callback or None."
            _LOG.error(err_message)
            raise TypeError(err_message)

        if self.nav_thread is None:
            self.nav_thread = DemoNavThread(callback)
            self.nav_thread.start()
            _LOG.debug("Nav thread started")
        else:
            self.nav_thread.change_callback(callback)
            self.nav_thread.start()
            _LOG.debug("Changed callback")

    def set_config(
        self, activate_gps: bool = True, activate_navdata: bool = True
    ) -> None:
        """Setter for configurations (gps, navdata)

        Args:
            activate_gps (bool, optional): Flag for starting gps. Defaults to True.
            activate_navdata (bool, optional): Flag for starting navdata. Defaults to True.
        """

    def print_navdata(self, navdata: dict) -> None:
        """Trivial function for prining Navdata
        Should be used as a callback.

        Args:
            navdata (dict): Navigation data to be printed
        """
        print(navdata)

    def takeoff(self) -> None:
        """Simulate taking off"""
        _LOG.info("Takeoff")

    def land(self) -> None:
        """Simulate landing"""
        _LOG.info("Land")

    def calibrate(self) -> None:
        """Simulate caliberation"""
        _LOG.info("Calibrate")

    def forward(self) -> None:
        """Simulate forward movement"""
        _LOG.info("Forward")

    def backward(self) -> None:
        """Simulate backward movement"""
        _LOG.info("Backward")

    def left(self) -> None:
        """Simulate left movement"""
        _LOG.info("Left")

    def right(self) -> None:
        """Simulate right movement"""
        _LOG.info("Right")

    def up(self) -> None:
        """Simulate up movement"""
        _LOG.info("Up")

    def down(self) -> None:
        """Simulate down movement"""
        _LOG.info("Down")

    def rotate_left(self) -> None:
        """Simulate left rotation"""
        _LOG.info("Rotating left")

    def rotate_right(self) -> None:
        """Simulate right rotation"""
        _LOG.info("Rotating right")

    def hover(self) -> None:
        """Simulate hover movement"""
        _LOG.info("Hover")

    def emergency(self) -> None:
        """Simulate emergency"""
        _LOG.info("Emergency")

    def stop(self):
        """Simulate stopping"""
        self.is_connected = False
        if self.video_thread is not None:
            self.video_thread.stop()
            self.video_thread.join()
            _LOG.debug("Video thread stopped")

        if self.nav_thread is not None:
            self.nav_thread.stop()
            self.nav_thread.join()
            _LOG.debug("Nav thread stopped")

        _LOG.warning("Drone disconnected")

    def reset(self):
        """Simulate resting"""
        _LOG.info("Reseting")


class DemoVideoThread(Thread):
    """Demo for video thread"""

    def __init__(
        self,
        close_callback: Callable,
        model: CVModel,
        video_index: Union[str, int] = 0,
        frame_name: str = "Demo Video Capture",
    ) -> None:

        super().__init__()
        self.close_callback = close_callback
        self.model = model
        self.frame_name = frame_name
        self.video_index = video_index
        self.running = True

    def run(self):
        """Run video stream
        This method is invoked by the internal method of
        `threading.Thread` under the name `start`.

        To start this thread, call `DemoVideoThread(...).start()`
        """
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            _LOG.warning("Error while trying to read video. Please check path again")

        prev_time = 0
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

        _LOG.debug("Closing Video Stream ...")
        cap.release()
        cv2.destroyAllWindows()
        self.close_callback()

    def change_model(self, model: CVModel):
        """Change computer vision model running on the video stream"""
        self.model = model
        _LOG.debug("model for video thread changed")

    def stop(self):
        """Stop the running thread"""
        self.running = False


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
