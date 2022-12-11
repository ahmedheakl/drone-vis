from dronevis.detection_torch import FasterRCNN

model = FasterRCNN()
model.load_model()
model.detect_webcam(video_index="tcp://192.168.1.1:5555", window_name="Drone Detection")
