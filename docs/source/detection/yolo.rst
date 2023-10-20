YOLO
====

`You Only Look Once (YOLO) <https://arxiv.org/abs/1506.02640>`_. is the most popular and efficient model in computer vision. Introduced in 2015 to be trained end-to-end, it aimed at real-time object detection and classification. The model family belongs to one-stage object detection models that process an entire image in a single forward pass of a CNN. Unlike two-stage detection models such as R-CNN and its variants – first propose regions of interest and then, classify these regions- YOLO processes the entire image in a single pass, making it exceedingly faster.

YOLOv5 Torch
------------

`YOLOv5 <https://docs.ultralytics.com/yolov5/>`_, developed by ultralytics, used YOLOv3 head network, however, introduced a new backbone network called EfficientDet. Furthermore, significant improvements have been made to boost the detection speed and increase the accuracy.

- **Dynamic Anchor Assignment**: adjusting the anchor boxes used during training to better fit the distribution of object sizes in the dataset.

- **Improved Data Augmentation**: improves model capabilities in difficult lighting conditions, as well as in situations where the objects are occluded. 
            
- **Modified Non-Maximum Suppression**: more efficient and accurate version was developed to improve overall detection performance.

YOLOv5 became the world's state-of-the-art repo for object detection back in 2020 given its flexible Pythonic structure. Evaluated on MS COCO dataset test-dev 2017, YOLOv5x achieved an AP of 50.7% with an image size of 640 pixels. Using a batch size of 32, it can achieve a speed of 200 FPS on an NVIDIA V100. 


.. autoclass:: dronevis.models.YOLOv5

YOLOv8 Interface
----------------

.. autoclass:: dronevis.models.yolov8.YOLOv8


YOLOv8 Detection Torch
------------

`YOLOv8 <https://docs.ultralytics.com/>`_ is the last model in the YOLO series (at the time of developing our work), surpassing all of them in both accuracy and speed. YOLOv8 introduced minor changes, e.g., removal/addition of some CNN layers or changing the kernel sizes), yet the major change was anchor-free detections. YOLOv8 predicts the center of an object directly instead of the offset from a known anchor box. It is more flexible as it does not require the manual specification of anchor boxes, which can be difficult to choose and can lead to sub-optimal results in previous models of YOLO. In addition, YOLOv8 introduced multiple models for solving other common tasks in computer vision – Instance Segmentation, Image Classification, Object Tracking.  
Evaluated on MS COCO dataset test-dev 2017, YOLOv8x achieved an AP of 53.9% with an image size of 640 pixels (compared to 50.7% of YOLOv5 on the same input size) with a speed of over 500 FPS on a TensorRT.

.. autoclass:: dronevis.models.YOLOv8Detection
