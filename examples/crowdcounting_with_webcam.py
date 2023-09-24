from dronevis.models.croud_count import CrowdCounter

model = CrowdCounter()
model.load_model()
model.detect_webcam("archery.mp4")
