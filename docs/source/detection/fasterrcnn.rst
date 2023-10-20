Faster R-CNN
============

`Faster Region-based CNN (R-CNN) <https://arxiv.org/abs/1506.01497>`_ is a significant advancement over its predecessors, `R-CNN <https://arxiv.org/pdf/1311.2524.pdf>`_  and `Fast R-CNN <https://arxiv.org/pdf/1504.08083.pdf>`_.
It incorporates region proposal generation within the network architecture, eliminating the need for external algorithms. In traditional approaches, region proposals were generated
using `selective search <http://www.huppelen.nl/publications/selectiveSearchDraft.pdf>`_, which could be time-consuming. Fast R-CNN improved upon this by performing a single forward pass of the CNN on the entire input
image, generating region proposals based on the extracted features. However, Faster R-CNN further enhanced the architecture by introducing a Region Proposal Network (RPN). The RPN
shares convolutional layers with the object detection network and generates region proposals by sliding a small network window over the feature map. Simultaneously, it predicts
objectness scores and refines bounding box coordinates. The Faster R-CNN architecture enables end-to-end training and faster inference by efficiently sharing convolutional layers
between the RPN and the object detection network.


Faster R-CNN Torch
------------------

.. autoclass:: dronevis.models.FasterRCNN