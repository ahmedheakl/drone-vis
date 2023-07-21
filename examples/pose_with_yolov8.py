"""Example usage for pose estimation using YOLOv8"""
from dronevis.models import YOLOv8Pose

model = YOLOv8Pose()
model.load_model()
model.detect_webcam(track=True)
