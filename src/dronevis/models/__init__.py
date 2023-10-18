"""Retrieve models imports for information hiding software priciple"""
from dronevis.abstract.noop_model import NOOPModel
from dronevis.models.faster_rcnn_torch import FasterRCNN
from dronevis.models.face_detection import FaceDetectModel
from dronevis.models.pose_mediapipe import PoseSegEstimation
from dronevis.models.ssd_torch import SSD
from dronevis.models.yolov5_torch import YOLOv5
from dronevis.models.gesture_recognition import GestureRecognition
from dronevis.models.yolov8 import YOLOv8Detection, YOLOv8Segmentation, YOLOv8Pose
from dronevis.models.depth_estimation import DepthEstimator
from dronevis.models.action_recognition import ActionRecognizer
from dronevis.models.croud_count import CrowdCounter
from dronevis.models.road_segmentation import RoadSegmentation, LaneDetection
from dronevis.models.haar_face_detection import HaarFaceDetection
from dronevis.models.cnn_face_detection import CNNFaceDetection
from dronevis.models.dnn_face_detection import DNNFaceDetection
from dronevis.models.hog_face_detection import HOGFaceDetection


models_list = {
    "None": NOOPModel,
    "SSD": SSD,
    "Face": FaceDetectModel,
    "YOLOv5": YOLOv5,
    "Faster R-CNN": FasterRCNN,
    "Pose": PoseSegEstimation,
    "Segment": PoseSegEstimation,
    "Pose+Segment": PoseSegEstimation,
    "YOLOv8Detect": YOLOv8Detection,
    "YOLOv8Pose": YOLOv8Pose,
    "YOLOv8Segment": YOLOv8Segmentation,
    "YOLOv8Track": YOLOv8Detection,
    "ActionGoogle": ActionRecognizer,
    "ActionFacebook": ActionRecognizer,
    "ActionMCG": ActionRecognizer,
    "DepthEstimator": DepthEstimator,
    "RoadSegmentation": RoadSegmentation,
    "LaneDetection": LaneDetection,
    "HaarFaceDetector": HaarFaceDetection,
    "HOGFaceDetector": HOGFaceDetection,
    "CNNFaceDetector": CNNFaceDetection,
    "DNNFaceDetector": DNNFaceDetection,
}
