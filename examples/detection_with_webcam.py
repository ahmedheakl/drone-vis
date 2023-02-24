from dronevis.detection_torch.yolov5_torch import YOLOv5

model = YOLOv5()
model.load_model()
model.detect_webcam()
