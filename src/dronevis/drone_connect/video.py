import threading
import cv2
import time

class Video(threading.Thread):
    """Connect video stream from drone

    Args:
        threading (Thread): thread for video stream
    """
    def __init__(self, ip: str = "192.168.1.1", model=None) -> None:
        """Initialize drone instance

        Args:
            ip (str, optional): ip of the drone. Defaults to "192.168.1.1".
        """
        self.ip = ip
        self.video_port = 5555
        self.socket_lock = threading.Lock()
        self.protocol = "tcp"
        self.cam_connect = f'{self.protocol}://{self.ip}:{self.video_port}'
        self.frame_name = "Video Capture"
        self.is_stream = False
        self.cap = None
        self.detection = True
        self.model = model
        threading.Thread.__init__(self)

    def run(self) -> None:
        """Create video stream and view frames
        """
        """Detecting objects with a webcam using FasterRCNN model
        (to quit running this function press 'q')"""
        
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.cam_connect)
            if not self.cap.isOpened():
                print("Error while trying to read video. Please check path again")
        self.is_stream = True
        while self.cap.isOpened():
            self.socket_lock.acquire()
            if not self.is_stream:
                self.socket_lock.release()
                break
            running, frame = self.cap.read()
                
            if running:
                if self.detection:
                    frame, wait_time = self.model.frame_detection(frame)
                else:
                    wait_time = 1
                    fps = self.cap.get(cv2.CAP_PROP_FPS)
                    cv2.putText(
                        frame,
                        f"{fps:.3f} FPS",
                        (15, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )
                cv2.imshow("Drone connection", frame)
                if cv2.waitKey(wait_time) & 0xFF == ord("q"):
                    break
            else:
                print('error reading video feed')
            self.socket_lock.release()
        print("Stream Closed ...")
        self.cap.release()
        cv2.destroyAllWindows()
        