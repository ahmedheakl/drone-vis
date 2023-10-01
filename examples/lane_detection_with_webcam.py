"""Example of lane detection with webcam."""
from dronevis.models import LaneDetection

model = LaneDetection()
model.load_model()
model.detect_webcam()
