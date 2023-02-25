"""Pose estimation via user camera"""
from dronevis.pose import PoseSegEstimation

model = PoseSegEstimation()
model.load_model()
model.detect_webcam()
