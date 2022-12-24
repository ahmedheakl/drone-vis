# from dronevis.detection_torch.yolov5_torch import YOLOv5

# model = YOLOv5()
# model.load_model()
# model.detect_webcam()

from dronevis.detection_torch import SSD
import numpy as np

image = np.zeros((10, 10), dtype=np.float32)

model = SSD()
model.predict(image)