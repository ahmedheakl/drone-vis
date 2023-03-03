"""Pose estimation via user camera"""
from dronevis.models import PoseSegEstimation

model = PoseSegEstimation()
model.load_model()
model.detect_webcam()
