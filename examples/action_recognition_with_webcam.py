"""Example usage for action recognition with webcam"""
from dronevis.models.action_recognition import ActionRecognizer

model = ActionRecognizer()
model.load_model()
model.detect_webcam()
