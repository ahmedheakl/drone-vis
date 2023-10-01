"""Example of road segmentation with webcam."""
from dronevis.models import RoadSegmentation

model = RoadSegmentation()
model.load_model()
model.detect_webcam()
