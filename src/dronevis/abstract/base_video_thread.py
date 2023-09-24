"""Interface for video thread"""
# mypy: ignore-errors
import threading
from typing import Callable, Union
import logging
import time
import cv2

from dronevis.utils.general import write_fps
from dronevis.models.model_factory import ModelFactory

_LOG = logging.getLogger(__name__)


class Singleton(type):
    """Signleton meteclass implementation"""

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
        operation_callback: Callable,
        model_name: str,
        ip_address: str = "192.168.1.1",
        video_index: Union[int, str] = 0,
    ):
        if not hasattr(closing_callback, "__call__"):
            err_message = "Close callback provided is not callable"
            _LOG.critical(err_message)
            raise TypeError(err_message)

        if not hasattr(operation_callback, "__call__"):
            err_message = "Operation callback provided is not callable"
            _LOG.critical(err_message)
            raise TypeError(err_message)

        if model_name not in ModelFactory.models_list:
            err_message = f"Model {model_name} is not supported"
            _LOG.critical(err_message)
            raise ValueError(err_message)

        super().__init__()
        self.close_callback = closing_callback
        self.operation_callback = operation_callback
        self.ip_address = ip_address
        self.model = ModelFactory.create_model(model_name)
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
        prev_time = time.perf_counter()
        while not self.is_stopped:
            fps = 1 / (time.perf_counter() - prev_time)
            prev_time = time.perf_counter()
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
                _LOG.warning("Stop reading the video stream")
                break

            if not self._show_window:
                _LOG.critical("Showing frames ...")
                continue

            self.is_destroyed = False
            output_image = self.model.predict(frame)
            output_image = write_fps(output_image, fps)
            self.operation_callback(output_image, frame)
            predict_time = int((time.perf_counter() - prev_time) * 1000)
            if predict_time > 30:
                continue
            time.sleep((30 - predict_time) / 1000)

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

    def change_model(self, model_name: str):
        """Change computer vision model running on the video stream"""

        self.model = ModelFactory.create_model(model_name)
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
