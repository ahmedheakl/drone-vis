"""Tracking via stored video"""
import os
from dronevis.models import HumanTracking


human_tracking = HumanTracking()
parent_dir = os.path.dirname(os.getcwd())
human_tracking.detect_video(
    os.path.join(parent_dir, r"input_videos/Pedestrian video.avi"),
    os.path.join(parent_dir, r"output_videos/out1.mp4"),
)
