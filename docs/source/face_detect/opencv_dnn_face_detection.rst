OpenCV DNN Face Detection
=========================

`OpenCV has also implemented a deep neural network (DNN) <https://docs.opencv.org/4.x/d0/dd4/tutorial_dnn_face.html>`_ based face detector since version 3.3.
This model is based on a single-shot multibox detector and utilizes the ResNet-10 architecture as the backbone. It uses a combination of feature extraction
and classification techniques to detect faces in images. The feature extraction step involves extracting relevant information from the input image, such as
edges, lines, and corners, using a series of Haar-like features. The extracted features are then fed into a CNN, which uses a ResNet-10 architecture to
classify the features as either face or non-face. It achieve an accuracy of 99.60% on the LFW dataset. However, one potential drawback of the DNN face
detector in OpenCV is its higher computational cost compared to the Haar cascade classifier. This may make it less suitable for resource-constrained devices
such as smartphones or embedded systems.


Example:

.. code-block:: python

    from dronevis.models import DNNFaceDetection

    model = DNNFaceDetection()
    model.load_model()
    model.detect_webcam()

OpenCV DNN Face Detection Class
-------------------------------

.. autoclass:: dronevis.models.DNNFaceDetection