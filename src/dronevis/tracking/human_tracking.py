# Import libraries
import cv2
import numpy as np
from typing import Union
import time
import os
import urllib.request
import torch
import os.path
from dronevis.utils import find

from dronevis.abstract.abstract_torch_model import CVModel
from dronevis.config.config import COCO_NAMES_v4

WEIGHTS_PATH = "yolov4.weights"
WEIGHTS_LINK = "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights"

CONFIG_PATH = "yolov4.cfg"
CONFIG_LINK = "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.cfg"

class HumanTracking(CVModel):
    """ 
    Human Tracking and detction using DeepSORT Algorthim based on YOLO4

    """

    class_names = COCO_NAMES_v4

    def __init__(self,confidence_threshold:int = 0.25,non_maximum_supression_thershold:int = 0.4) -> None:
        """
        Initialize HumanTracking model
        
        Args:
            confidence_threshold (int): thershold to detect humans 
            non_maximum_supression_thershold (int): thershold to prevent overlapping detections to the same person
            (both can be increased to provide more acuracte results)
        """
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = non_maximum_supression_thershold

    def load_model(self)-> None:
        """
        Load YOLO v4 model using the configration file and weights of YOLO v4
        Initialize DeepSORT tracker
        """
        from deep_sort_realtime.deepsort_tracker import DeepSort
        yolo_cfg_path = find (CONFIG_PATH)
        if yolo_cfg_path == None:
            print("Downloading Faster YOLO v4 configuration...")
            yolo_cfg_path, headers = urllib.request.urlretrieve(
                CONFIG_LINK, 
                filename= os.path.join(os.getcwd(),CONFIG_PATH),
                )
        
        yolo_weights_path = find (WEIGHTS_PATH)
        if yolo_weights_path == None:
            print("Downloading Faster YOLO v4 weights...")
            yolo_weights_path, headers = urllib.request.urlretrieve(
                WEIGHTS_LINK, 
                filename= os.path.join(os.getcwd(),WEIGHTS_PATH),
                )
        print("Loading Faster YOLO v4 model ...")
        self.model = cv2.dnn.readNet(yolo_cfg_path, yolo_weights_path)
        self.tracker = DeepSort()


    def transform_img(self, image: np.ndarray) -> np.ndarray:
        """Idle transformation.

        **Implemented just for code integrity**


        Args:
            image (np.ndarray): input image

        Returns:
            np.ndarray: output image
        """
        return image

    def predict(self,image:np.ndarray) -> list:
        """
        Detect Humans in an image using YOLO v4
        Args:
            image (np.ndarray): input image
        Returns:
            List of Detections, where each detection is represented as a tuple
            of bounding box coordinates, classid and score
        """
        detections = []
        model = cv2.dnn_DetectionModel(self.model)
        model.setInputParams(size=(416, 416), 
                             scale=1/255, 
                             swapRB=True,
                             )
        classes, scores, boxes = model.detect(
            frame=image,
            confThreshold=self.confidence_threshold, 
            nmsThreshold=self.nms_threshold,
            )
        for (classid, score, box) in zip(classes, scores, boxes):
            label = HumanTracking.class_names[classid[0]]
            if (label == "person"):
                detections.append((box,classid,score))
        return detections
    

    def detect_webcam(self,video_index: Union[str, int] = 0, window_name: str = "Cam Detection") -> None:
        """Start webcam detection from video_index
        *(to quit running this function press 'q')*
        Args:
            video_index (Union[str, int], optional): index of video stream device. Defaults to 0 (webcam).
            window_name (str, optional): name of cv2 window. Defaults to "Cam Detection".
        """
        self.load_model()

        cap = cv2.VideoCapture(video_index)
        prev_time = 0.0
        while True:
            _, frame = cap.read()
            detections = self.predict(frame)
            # Update object tracks with DeepSORT
            is_detection = True
            if (len(detections) == 0):
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
                    
                cur_time = time.time()
                fps = 1 / (cur_time - prev_time)
                cv2.imshow(window_name,frame)
                prev_time = cur_time
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        cv2.destroyAllWindows()
        cap.release()

    def detect_video(self,video_path:str,output_path:str)->None:
        """Start webcam detection from video_index
        Args:
            video_path (str): path to input video (input video should be in input_videos folder).
            window_name (str): path to output video (output video should be in output_videos folder).
        """
        self.load_model()

        cap = cv2.VideoCapture(video_path)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        out = cv2.VideoWriter(
            filename=output_path, 
            fourcc=cv2.VideoWriter_fourcc(*'mp4v'),
            fps=30,
            frameSize=(frame_width, frame_height),
            )
        frame_count = 0 
        while True:
            success, frame = cap.read()
            if not success:
                break
            detections = self.predict(frame)
            # Update object tracks with DeepSORT
            is_detection = True
            if (len(detections) == 0):
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
        cap.release()
        out.release()



    


