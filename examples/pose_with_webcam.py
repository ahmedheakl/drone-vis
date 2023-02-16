from dronevis.pose import PoseSegEstimation

model = PoseSegEstimation()
model.load_model()
model.detect_webcam(is_seg=True)