"""Object detection via user webcam"""
from dronevis.models import YOLOv5

model = YOLOv5()
model.load_model()
model.detect_webcam()
