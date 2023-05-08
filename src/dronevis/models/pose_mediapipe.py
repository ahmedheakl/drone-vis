"""Module for pose estimation and single-instance human segmentation"""
import time
from typing import Union
import mediapipe as mp
import numpy as np
import cv2

from dronevis.utils.general import write_fps
from dronevis.abstract import CVModel


BG_COLOR = (0, 2, 102)
PERSON_BG_COLOR = (168, 29, 54)


class PoseSegEstimation(CVModel):
    """Pose estimation class for loading and predicting with mediapipe
    ``BlazePose`` model.

    The model inherits from base ``CVModel`` and implements its abstract
    methods: ``load_model``, ``transform_img``, ``predict``, ``detect_webcam``.
    """

    def __init__(self, is_seg: bool = False, is_seg_pose: bool = False):
        assert is_seg + is_seg_pose < 2, "You can only choose one model mode"

        self.pose_module = mp.solutions.pose  # type: ignore
        self.drawer = mp.solutions.drawing_utils  # type: ignore
        self.net = None
        self.is_seg = is_seg
        self.is_seg_pose = is_seg_pose

    def load_model(self) -> None:
        """Load model from weights associated with mediapipe"""
        self.net = self.pose_module.Pose(enable_segmentation=True)

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Transform image from ``BGR`` to ``RGB``

        Args:
            image (np.array): input image

        Returns:
            np.array: transformed image
        """
        image = np.asarray(image)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def predict(
        self,
        image: np.ndarray,
        is_seg: bool = False,
        is_seg_pose=False,
        all_formats: bool = False,
    ):
        """Predict keypoints for pose and draw them on input image.
        **Input image is assumed to be BGR**.

        Args:
            image (np.array): input image
            is_seg (bool, optional): flag whether a segmentation is desired. Defaults to False.
            all_formats (bool, optional): flag whether to return all image format (segmentation,
            pose estimation, and pose-segmentation). Defaults to False.

        Returns:
            Tuple[np.array, ...]: output image with keypoints drawn, segmented image
            segmented image with pose points
        """
        is_seg |= self.is_seg
        is_seg_pose |= self.is_seg_pose

        assert self.net, "You need to load the model first. Please run ``load_model``."
        assert is_seg + is_seg_pose < 2, "You can only choose one model mode"

        image = self.transform_img(image)
        res = self.net.process(image)
        seg_image = image.copy()
        if not res.pose_landmarks:
            return [cv2.cvtColor(image, cv2.COLOR_BGR2RGB)] * 3

        if is_seg or is_seg_pose:
            seg_mask = res.segmentation_mask
            condition = np.stack([seg_mask] * 3, axis=-1) > 0.1
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            person_bg = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            person_bg[:] = PERSON_BG_COLOR
            seg_image = np.where(condition, bg_image, person_bg)

        self.drawer.draw_landmarks(
            image,
            res.pose_landmarks,
            self.pose_module.POSE_CONNECTIONS,
        )
        seg_pose_image = seg_image.copy()
        self.drawer.draw_landmarks(
            seg_pose_image,
            res.pose_landmarks,
            self.pose_module.POSE_CONNECTIONS,
        )
        if all_formats:
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), seg_image, seg_pose_image

        if is_seg:
            return seg_image

        if is_seg_pose:
            return seg_pose_image

        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def detect_webcam(
        self,
        video_index: Union[str, int] = 0,
        window_name: str = "Pose",
    ) -> None:
        """Start webcam pose estimation from video_index
        *(to quit running this function press 'q')*

        The stream is retrieved and decoded using `opencv library <https://opencv.org/>`_.

        Args:
            video_index (int | str, optional): index of video stream device. Defaults to 0.
            window_name (str, optional): name of cv2 window. Defaults to "Pose".
            is_seg (bool, optional): flag whether a segmentation is desired. Defaults to False.
        """
        cap = cv2.VideoCapture(video_index)
        prev_time = 0.0

        while True:
            _, image = cap.read()
            image, seg, seg_pose = self.predict(image, all_formats=True)

            cur_time = time.time()
            fps = 1 / (cur_time - prev_time)
            prev_time = cur_time
            cv2.imshow(window_name, write_fps(image, fps))

            cv2.imshow(window_name + "Segmentation", write_fps(seg, fps))
            cv2.imshow("Segmented Pose", write_fps(seg_pose, fps))

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()
        cap.release()
