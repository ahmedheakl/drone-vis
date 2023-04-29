"""Example usage for object segmentation using YOLOv8"""
from dronevis.models import YOLOv8Segmentation

model = YOLOv8Segmentation()
model.load_model()
model.detect_webcam(track=True)
