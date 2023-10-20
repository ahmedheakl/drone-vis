MediaPipe Face Detection
========================

`The MediaPipe Face Classifier <https://developers.google.com/mediapipe/solutions/vision/face_landmarker>`_ is a deep learning-based approach to face detection that uses a novel architecture to improve upon traditional computer vision models.
Proposed by Google researchers, the MediaPipe Face Classifier is based on a multi-task learning framework that jointly optimizes a face detection task and a face classification task. The model uses a combination of convolutional neural networks (CNNs) and recurrent neural networks (RNNs) to extract features from face images
and classify them into different categories. One of the key advantages of the MediaPipe Face Classifier is its ability to handle diverse poses and lighting conditions. Evaluated on 
the "Labeled Faces in the Wild" (LFW) dataset, where it achieved an accuracy of 99.63% with a false positive rate of 0.17. In addition to its high accuracy,
the MediaPipe Face Classifier is also computationally efficient. The model can be deployed on resource-constrained devices, such as smartphones or drones, making it a promising solution
for real-world face detection applications. It has a major drawback though making it hard to use for drone applications, i.e. the model is only applicable for close-up faces; it almost
does not detect faces for distant people.

Example
-------

.. code-block:: python

    from dronevis.models import FaceDetectModel
    
    model = FaceDetectModel()    # create model instance
    model.load_model()           # load model weights 
    model.detect_webcam()        # run camera detection


Face Detection Class
--------------------


.. autoclass:: dronevis.models.FaceDetectModel