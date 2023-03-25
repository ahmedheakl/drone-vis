"""Interface for video thread"""
import threading
from typing import Callable, Union
import logging
import time
import cv2
from inspect import getmro

from dronevis.abstract.abstract_model import CVModel
from dronevis.utils.general import write_fps

_LOG = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class BaseVideoThread(threading.Thread, metaclass=Singleton):
    """Abstract class for the video used in both `Drone` and `DemoDrone`"""

    frame_name = "Drone Capture"

    def __init__(
        self,
        closing_callback: Callable,
        model: CVModel,
        ip_address: str = "192.168.1.1",
        video_index: Union[int, str] = 0,
    ):
        if CVModel not in getmro(type(model)):
            err_message = "Model provided is not an instance of ``CVModel``"
            _LOG.error(err_message)
            raise TypeError(err_message)

        if not hasattr(closing_callback, "__call__"):
            err_message = "Callback provided is not callable"
            _LOG.critical(err_message)
            raise TypeError(err_message)

        super().__init__()
        self.close_callback = closing_callback
        self.ip_address = ip_address
        self.model = model
        self.running = False
        self._video_index = video_index
        self.is_stopped = False
        self.is_destroyed = True
        self.cap = cv2.VideoCapture(self._video_index)
        self._show_window = True
        self.start()

    def run(self) -> None:
        """Create video stream and view frames"""
        if not self.cap.isOpened():
            _LOG.warning("Error while trying to read video. Please check path again")

        prev_time = 0.0
        while not self.is_stopped:
            if not self.running:
                if not self.is_destroyed:
                    cv2.destroyWindow(self.frame_name)
                    self.cap.release()
                    self.is_destroyed = True
                continue

            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(self._video_index)

            status, frame = self.cap.read()

            if not status:
                continue

            if not self._show_window:
                _LOG.critical("Showing frames ...")
                continue

            self.is_destroyed = False
            frame = self.model.predict(frame)
            cur_time = time.time()
            fps = 1 / (cur_time - prev_time)
            prev_time = cur_time
            cv2.imshow(self.frame_name, write_fps(frame, fps))

            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.stop()

        _LOG.info("Closing video stream ...")
        self.cap.release()
        cv2.destroyAllWindows()
        self.close_callback()
        _LOG.info("Closed video stream")

    @property
    def video_index(self) -> Union[str, int]:
        """Getter for video index property"""
        return self._video_index

    @video_index.setter
    def video_index(self, index: Union[str, int]) -> None:
        """Setter for video index property"""
        self._video_index = index
        self.cap = cv2.VideoCapture(self._video_index)

    @property
    def show_window(self) -> bool:
        """Getter for show window property"""
        return self._show_window

    @show_window.setter
    def show_window(self, is_shown: bool) -> None:
        """Setter for show window property"""
        self._show_window = is_shown

    def change_model(self, model: CVModel):
        """Change computer vision model running on the video stream"""

        if CVModel not in getmro(type(model)):
            err_message = "Model provided is not an instance of ``CVModel``"
            _LOG.error(err_message)
            raise TypeError(err_message)

        self.model = model
        _LOG.debug("Model for video thread changed")

    def stop(self) -> None:
        """Stop the running video thread"""
        self.running = False

    def resume(self) -> None:
        """Resume running the thread and video capture"""
        self.running = True

    def close_thread(self) -> None:
        """Irrecoverably closing the thread"""
        self.is_stopped = True
