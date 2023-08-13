"""Example usage of depth estimation model"""
from dronevis.models import DepthEstimator

model = DepthEstimator()
model.load_model()
model.detect_webcam()
