from dronevis.detection_torch import FasterRCNN

model = FasterRCNN()
model.load_model()
model.detect_webcam()
