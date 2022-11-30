import socket
import threading
from dronevis.drone_connect.video import Video
class Drone():
    def __init__(self):
        self.command_port = 5556
        self.data_port = 5554

    def connect_video(self,ip = "192.168.1.1"):
        self.ip = ip
        self.video_thread = Video(self.ip)
        self.video_thread.run()