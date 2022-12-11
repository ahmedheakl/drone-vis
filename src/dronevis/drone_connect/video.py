import threading
import socket
import cv2

class Video(threading.Thread):
    """Connect video stream from drone

    Args:
        threading (Thread): thread for video stream
    """
    def __init__(self, ip: str = "192.168.1.1") -> None:
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
        threading.Thread.__init__(self)

    def run(self) -> None:
        """Create video stream and view frames
        """
        cam = cv2.VideoCapture(self.cam_connect)
        self.running = True
        while self.running:
            # get current frame of video
            self.socket_lock.acquire()
            self.running, frame = cam.read()
            if self.running:
                cv2.imshow(self.frame_name, frame)
                if cv2.waitKey(1) & 0xFF == 27: 
                    # escape key pressed
                    self.running = False

            else:
                # error reading frame
                print('error reading video feed')
            self.socket_lock.release()
        cam.release()
        cv2.destroyAllWindows()
