from dronevis.pose import PoseEstimation

model = PoseEstimation()
model.load_model()
model.detect_webcam()