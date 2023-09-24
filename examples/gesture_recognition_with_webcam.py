"""Gesture Recognition via user camera"""
from dronevis.models import GestureRecognition

model = GestureRecognition()
model.load_model()
model.detect_webcam("sample_dance.mp4")
