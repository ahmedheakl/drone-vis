"""Module for pose estimation and single-instance human segmentation"""

import time
from dronevis.abstract import CVModel
import mediapipe as mp
import numpy as np
import cv2
from dronevis.utils.image_process import write_fps

BG_COLOR = (0, 2, 102)
PERSON_BG_COLOR = (168, 29, 54)


class PoseSegEstimation(CVModel):
    """Pose estimation class for loading and predicting with mediapipe
    ``BlazePose`` model.

    The model inherits from base ``CVModel`` and implements its abstract
    methods: ``load_model``, ``transform_img``, ``predict``, ``detect_webcam``.
    """

    def __init__(self):
        self.pose_module = mp.solutions.pose
        self.drawer = mp.solutions.drawing_utils
        self.net = None

    def load_model(self):
        """Load model from weights associated with mediapipe"""
        self.net = self.pose_module.Pose(enable_segmentation=True)

    def transform_img(self, image):
        """Transform image from ``BGR`` to ``RGB``

        Args:
            image (np.array): input image

        Returns:
            np.array: transformed image
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def predict(self, image, is_seg=False):
        """Predict keypoints for pose and draw them on input image.
        **Input image is assumed to be BGR**.

        Args:
            image (np.array): input image
            is_seg (bool, optional): flag whether a segmentation is desired. Defaults to False.

        Returns:
            Tuple[np.array, ...]: output image with keypoints drawn, segmented image
            segmented image with pose points
        """
        assert self.net, "You need to load the model first. Please run ``load_model``."
        image = self.transform_img(image)
        res = self.net.process(image)
        seg_image = image.copy()
        if not res.pose_landmarks:
            return [cv2.cvtColor(image, cv2.COLOR_BGR2RGB)] * 3
        if is_seg:
            seg_mask = res.segmentation_mask
            condition = np.stack([seg_mask] * 3, axis=-1) > 0.1
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            person_bg = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            person_bg[:] = PERSON_BG_COLOR
            seg_image = np.where(condition, bg_image, person_bg)
        self.drawer.draw_landmarks(
            image, res.pose_landmarks, self.pose_module.POSE_CONNECTIONS
        )
        seg_pose_image = seg_image.copy()
        self.drawer.draw_landmarks(
            seg_pose_image, res.pose_landmarks, self.pose_module.POSE_CONNECTIONS
        )
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), seg_image, seg_pose_image

    def detect_webcam(self, video_index=0, window_name="Pose", is_seg=False):
        """Start webcam pose estimation from video_index
        *(to quit running this function press 'q')*

        The stream is retrieved and decoded using `opencv library <https://opencv.org/>`_.

        Args:
            video_index (int | str, optional): index of video stream device. Defaults to 0.
            window_name (str, optional): name of cv2 window. Defaults to "Pose".
            is_seg (bool, optional): flag whether a segmentation is desired. Defaults to False.
        """
        cap = cv2.VideoCapture(video_index)
        prev_time = 0

        while True:
            _, image = cap.read()
            image, seg, seg_pose = self.predict(image, is_seg)

            cur_time = time.time()
            fps = 1 / (cur_time - prev_time)
            prev_time = cur_time
            cv2.imshow(window_name, write_fps(image, fps))
            if is_seg:
                cv2.imshow(window_name + "Segmentation", seg)
                cv2.imshow("Segmented Pose", seg_pose)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()
        cap.release()

if __name__ == "__main__":
    model = PoseSegEstimation()
    model.load_model()
    model.detect_webcam(is_seg=True)