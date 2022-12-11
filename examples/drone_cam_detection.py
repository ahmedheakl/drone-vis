from dronevis.detection_gluoncv import Yolo

model = Yolo()
model.load_model()
model.detect_webcam(video_index="192.168.1.1", window_name="Drone Detection")
