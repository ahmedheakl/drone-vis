Haar Face Detection
===================

The Haar classifier is based on the Haar-like features proposed by `Viola and Jones <https://www.cs.cmu.edu/~efros/courses/LBMV07/Papers/viola-cvpr-01.pdf>`_. These features are simple rectangular filters that capture specific patterns in an image, such as edges, lines, and corners. The classifier works by applying a series of these Haar-like features to sub-regions of an image and evaluating the response at each stage to determine the likelihood of a face being present. The Haar classifier consists of a cascade of weak classifiers, which are trained using a variant of the AdaBoost algorithm. Evaluated on `Labeled Faces in the Wild (LFW) dataset <https://vis-www.cs.umass.edu/lfw/>`_, the classifier has demonstrated impressive results, achieving accuracies of over 95% with low false-positive rates.


Example: 

.. code-block:: python

    from dronevis.models import HaarFaceDetection

    model = HaarFaceDetection() # create model instance
    model.load()                # load model weights
    model.detect_webcam()       # run camera detection


Haar Face Detection Class
-------------------------

.. autoclass:: dronevis.models.HaarFaceDetection