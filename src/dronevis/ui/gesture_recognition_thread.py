"""Gesture Recognition Thread"""
from typing import Union
import threading
from tkinter.ttk import Label

from dronevis.models import GestureRecognition


class GestureThread(threading.Thread):
    """Thread for running the gesture recognition model"""

    def __init__(self, label: Label, video_index: Union[int, str] = 0):
        """Initialise the thread

        Args:
            label (Label): The label to update
        """
        super().__init__()
        self.model = GestureRecognition()
        self.model.load_model()
        self.video_index = video_index
        self.label = label
        self.running = True

    def run(self) -> None:
        """Run the thread"""
        self.model.on_frame_detect(self.label, self.video_index)
        self.running = False

    def resume(self) -> None:
        """Resume the thread"""
        self.model.on_frame_detect(self.label, self.video_index)
        self.running = False

    def stop(self) -> None:
        """Stop the thread"""
        self.model.stop_frame_detection()
        self.running = False
