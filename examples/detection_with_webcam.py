from dronevis.detection_gluoncv import Yolo

model = Yolo()
model.load_model()
model.detect_webcam()
