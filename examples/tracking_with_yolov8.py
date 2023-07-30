"""Human tracking using YOLOv8 with Detection, Pose Estimation or Segmentation"""
from dronevis.models import YOLOv8Detection

# from dronevis.models import YOLOv8Pose

# from dronevis.models import YOLOv8Segmentation

model = YOLOv8Detection()
model.load_model()
model.detect_webcam(track=True)
