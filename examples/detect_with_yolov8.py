"""Example usage for detection with YOLOv8"""
from dronevis.models import YOLOv8Detection


model = YOLOv8Detection()
model.load_model()
model.detect_webcam()
