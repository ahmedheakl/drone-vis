"""Retrieve video stream from the drone and run object detection on the obtained stream"""
from dronevis.detection_torch import FasterRCNN

PROTOCOL = "tcp"
VIDEO_PORT = 5555
DRONE_IP = f"{PROTOCOL}://192.168.1.1:{VIDEO_PORT}"

model = FasterRCNN()
model.load_model()
model.detect_webcam(video_index=VIDEO_PORT)
