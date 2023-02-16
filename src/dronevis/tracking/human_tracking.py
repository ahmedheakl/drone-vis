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

class HumanTracking(CVModel):
    """ 
    Human Tracking and detction using DeepSORT Algorthim based on YOLO4
    before using the class you need to install deep-sort-realtime using 
    the following command: pip install deep-sort-realtime  
    """
    def __init__(self,confedence_thershold:int = 0.25,non_maximum_supression_thershold:int = 0.4) -> None:
        """
        Initialize HumanTracking model and Load the model
        
        Args:
            confedence_thershold (int): thershold to detect humans 
            non_maximum_supression_thershold (int): thershold to prevent overlapping detections to the same person
            (both can be increased to provide more acuracte results)
        Note:
            YOLO v4 uses labels defined in coco_names.txt 
            (it is different than the ones defined in FasterRCNN)
        """
        
        self.class_names = COCO_NAMES_v4
        self.CONFIDENCE_THRESHOLD = confedence_thershold
        self.NMS_THRESHOLD = non_maximum_supression_thershold
        self.load_model()

    def load_model(self)-> None:
        """
        Load YOLO v4 model using the configration file and weights attached in tracker folder
        Initialize DeepSORT tracker
        """
        from deep_sort_realtime.deepsort_tracker import DeepSort
        yolo_cfg_path = find ("yolov4.cfg")
        if yolo_cfg_path == None:
            print("Downloading Faster YOLO v4 configuration...")
            yolo_cfg_path, headers = urllib.request.urlretrieve(
                "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.cfg", 
                filename= os.path.join(os.getcwd(),"yolov4.cfg"))
        
        yolo_weights_path = find ("yolov4.weights")
        if yolo_weights_path == None:
            print("Downloading Faster YOLO v4 weights...")
            yolo_weights_path, headers = urllib.request.urlretrieve(
                "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights", 
                filename= os.path.join(os.getcwd(),"yolov4.weights"))
        print("Loading Faster YOLO v4 model ...")
        self.model = cv2.dnn.readNet(yolo_cfg_path, yolo_weights_path)
        self.tracker = DeepSort()


    def transform_img(self, img: np.ndarray) -> torch.Tensor:
        """Transform image to tensor

        Args:
            img (numpy.ndarray): input array

        Returns:
            torch.Tensor: tensor img
        """
        assert self.transform is not None, "Model not initialized. You need to load the model first. Please run `load_model`."
        return self.transform(to_pil_image(img)).to(self.device)

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
        model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)
        classes, scores, boxes = model.detect(image, self.CONFIDENCE_THRESHOLD, self.NMS_THRESHOLD)
        for (classid, score, box) in zip(classes, scores, boxes):
            label = self.class_names[classid[0]]
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
        cap = cv2.VideoCapture(video_index)
        prev_time = 0
        while True:
            _, frame = cap.read()
            detections = self.predict(frame)
            # Update object tracks with DeepSORT
            Flag = True
            if (len(detections) == 0):
                Flag = False
            if Flag == True:
                tracks = self.tracker.update_tracks(detections, frame=frame)
                # Visualize object tracks
                for track in tracks:
                    bbox = track.to_tlbr()
                    cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 255, 255), 2)
                    cv2.putText(frame, str(track.track_id), (int(bbox[0]), int(bbox[1]) - 10), 0, 5e-3 * 200, (0, 255, 0), 2)
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
        cap = cv2.VideoCapture(video_path)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))
        frame_count = 0 
        while True:
            success, frame = cap.read()
            if not success:
                break
            detections = self.predict(frame)
            # Update object tracks with DeepSORT
            Flag = True
            if (len(detections) == 0):
                Flag = False
            if Flag == True:
                tracks = self.tracker.update_tracks(detections, frame=frame)
                # Visualize object tracks
                for track in tracks:
                    bbox = track.to_tlbr()
                    cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 255, 255), 2)
                    cv2.putText(frame, str(track.track_id), (int(bbox[0]), int(bbox[1]) - 10), 0, 5e-3 * 200, (0, 255, 0), 2)
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(image)
                frame_count = frame_count + 1
        cap.release()
        out.release()



    


