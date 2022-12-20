from dronevis.face_detection import FaceDetectModel

model = FaceDetectModel()
model.load_model()
model.detect_webcam()