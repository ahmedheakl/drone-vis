"""Implementation for human tracking model"""
from typing import Union
import wget
import cv2
import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort


from dronevis.utils.utils import find
from dronevis.abstract.abstract_torch_model import CVModel
from dronevis.config.config import COCO_NAMES_v4


# Those are the links to download the model weights if the user
# does not have them already.
WEIGHTS_PATH = "yolov4.weights"
CONFIG_PATH = "yolov4.cfg"
COMMON_LINK = (
    "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/"
)
WEIGHTS_LINK = COMMON_LINK + WEIGHTS_PATH
CONFIG_LINK = COMMON_LINK + CONFIG_PATH


class HumanTracking(CVModel):
    """
    Human Tracking and detction using DeepSORT Algorthim based on YOLO4
    """

    def __init__(
        self,
        confidence_threshold: float = 0.25,
        non_maximum_supression_thershold: float = 0.4,
    ) -> None:
        """
        Initialize HumanTracking model

        Args:
            confidence_threshold (int): thershold to detect humans
            non_maximum_supression_thershold (int): thershold to prevent overlapping
            detections to the same person
            (both can be increased to provide more acuracte results)
        """
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = non_maximum_supression_thershold
        self.model = None
        self.tracker = None

    def load_model(self) -> None:
        """
        Load YOLO v4 model using the configration file and weights of YOLO v4
        Initialize DeepSORT tracker
        """
        yolo_cfg_path = find(CONFIG_PATH)
        if yolo_cfg_path.strip() == "":
            print("Downloading Faster YOLO v4 configuration...")
            yolo_cfg_path = wget.download(CONFIG_LINK)
            print("")

        yolo_weights_path = find(WEIGHTS_PATH)
        if yolo_weights_path.strip() == "":
            print("Downloading Faster YOLO v4 weights...")
            yolo_weights_path = wget.download(WEIGHTS_LINK)
        print("Loading Faster YOLO v4 model ...")
        self.model = cv2.dnn.readNet(yolo_cfg_path, yolo_weights_path)
        self.tracker = DeepSort()

    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Idle transformation.

        **Implemented just for code integrity**
        """
        return image

    def predict(self, image: np.ndarray):
        """Detect Humans in an image using YOLO v4

        Returns:
            List: List of Detections, where each detection is represented as a tuple
            of bounding box coordinates, classid and score
        """
        if self.model is None:
            self.load_model()
        detections = []
        model = cv2.dnn_DetectionModel(self.model)
        model.setInputParams(
            size=(416, 416),
            scale=1 / 255,
            swapRB=True,
        )
        classes, scores, boxes = model.detect(
            frame=image,
            confThreshold=self.confidence_threshold,
            nmsThreshold=self.nms_threshold,
        )
        for (classid, score, box) in zip(classes, scores, boxes):
            label = COCO_NAMES_v4[classid]
            if label == "person":
                detections.append((box, classid, score))
        return detections

    def detect_webcam(
        self,
        video_index: Union[str, int] = 0,
        window_name: str = "Cam Detection",
    ) -> None:
        """Start webcam detection from video_index
        *(to quit running this function press 'q')*
        Args:
            video_index (Union[str, int], optional): index of video stream device.
            Defaults to 0 (webcam).
            window_name (str, optional): name of cv2 window. Defaults to "Cam Detection".
        """
        if self.tracker is None:
            self.load_model()

        assert self.tracker, "Tracker is not loaded properly"
        cap = cv2.VideoCapture(video_index)
        while True:
            _, frame = cap.read()
            detections = self.predict(frame)

            # Update object tracks with DeepSORT
            is_detection = True
            if len(detections) == 0:
                is_detection = False
            if is_detection:
                tracks = self.tracker.update_tracks(detections, frame=frame)
                # Visualize object tracks
                for track in tracks:
                    bbox = track.to_tlbr()
                    cv2.rectangle(
                        img=frame,
                        pt1=(int(bbox[0]), int(bbox[1])),
                        pt2=(int(bbox[2]), int(bbox[3])),
                        color=(255, 255, 255),
                        thickness=2,
                    )
                    cv2.putText(
                        img=frame,
                        text=str(track.track_id),
                        org=(int(bbox[0]), int(bbox[1]) - 10),
                        fontFace=0,
                        fontScale=5e-3 * 200,
                        color=(0, 255, 0),
                        thickness=2,
                    )
                cv2.imshow(window_name, frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        cv2.destroyAllWindows()
        cap.release()

    def detect_video(self, video_path: str, output_path: str) -> None:
        """Start webcam detection from video_index

        Args:
            video_path (str): Path to input video (should be in input_videos folder).
            output_path (str): Path to output video (should be in output_videos folder).
        """
        if self.tracker is None:
            self.load_model()

        assert self.tracker, "Something went wrong with loading the tracker"
        cap = cv2.VideoCapture(video_path)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        out = cv2.VideoWriter(
            filename=output_path,
            fourcc=cv2.VideoWriter_fourcc(*"mp4v"),
            fps=30,
            frameSize=(frame_width, frame_height),
        )
        frame_count = 0
        while True:
            _, frame = cap.read()
            detections = self.predict(frame)
            # Update object tracks with DeepSORT
            is_detection = True
            if len(detections) == 0:
                is_detection = False
            if is_detection:
                tracks = self.tracker.update_tracks(detections, frame=frame)
                # Visualize object tracks
                for track in tracks:
                    bbox = track.to_tlbr()
                    cv2.rectangle(
                        img=frame,
                        pt1=(int(bbox[0]), int(bbox[1])),
                        pt2=(int(bbox[2]), int(bbox[3])),
                        color=(255, 255, 255),
                        thickness=2,
                    )
                    cv2.putText(
                        img=frame,
                        text=str(track.track_id),
                        org=(int(bbox[0]), int(bbox[1]) - 10),
                        fontFace=0,
                        fontScale=5e-3 * 200,
                        color=(0, 255, 0),
                        thickness=2,
                    )
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(image)
                frame_count = frame_count + 1
