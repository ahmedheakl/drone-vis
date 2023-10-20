Single Shot Detector 
====================

The key innovation of `SSD <https://arxiv.org/pdf/1512.02325.pdf>`_ lies in the use of a single network that predicts object bounding boxes and class probabilities directly from feature maps at multiple scales. By employing a set of default bounding boxes of various aspect ratios and scales at each feature map location, SSD is able to efficiently detect objects of different sizes. The network architecture combines convolutional layers with several auxiliary convolutional layers to capture both low-level and high-level feature representations.\wg{What is the difference between the two sets of convolutional layers?} In contrast to Faster R-CNN, which requires a separate region proposal network, SSD performs object detection in a single pass, simplifying the pipeline and reducing computational cost.


SSD Torch 
---------

.. autoclass:: dronevis.models.SSD
