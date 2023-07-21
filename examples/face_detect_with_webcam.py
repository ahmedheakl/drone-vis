"""Face detection via user camera"""
from dronevis.models import FaceDetectModel

model = FaceDetectModel()
model.load_model()
model.detect_webcam()
