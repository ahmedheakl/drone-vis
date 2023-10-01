"""Example of using CrowdCounter class to count people in a webcam feed."""
from dronevis.models.croud_count import CrowdCounter

model = CrowdCounter()
model.load_model()
model.detect_webcam()
