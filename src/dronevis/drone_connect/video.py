import threading
import cv2
from dronevis.utils.utils import write_fps
from typing import Callable
import time
from dronevis.abstract import CVModel


class VideoThread(threading.Thread):
    """Connect video stream from drone

    Args:
        threading (Thread): thread for video stream
    """

    def __init__(
        self,
        closing_callback: Callable,
        model: CVModel,
        ip: str = "192.168.1.1",
    ) -> None:
        """Initialize drone instance

        Args:
            ip (str, optional): ip of the drone. Defaults to "192.168.1.1".
        """
        super(VideoThread, self).__init__()
        self.callback = closing_callback
        self.ip = ip
        self.video_port = 5555
        self.socket_lock = threading.Lock()
        self.protocol = "tcp"
        self.video_index = f"{self.protocol}://{self.ip}:{self.video_port}"
        self.frame_name = "Video Capture"
        self.running = True
        self.model = model
        self.close_callback = closing_callback

    def run(self) -> None:
        """Create video stream and view frames"""

        cap = cv2.VideoCapture(self.video_index)
        if not cap.isOpened():
            print("Error while trying to read video. Please check path again")

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

        print("Closing video stream ...")
        cap.release()
        cv2.destroyAllWindows()
        self.close_callback()

    def stop(self):
        self.running = False
