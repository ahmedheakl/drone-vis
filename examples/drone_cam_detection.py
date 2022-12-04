from dronevis.object_detection_models.ssd_torch import SSDTorch

model = SSDTorch()
model.load_model()
video_index = 'tcp://192.168.1.1:5555'
model.detect_webcam(video_index)
