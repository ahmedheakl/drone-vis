Dlib CNN Face Detection
=======================


`The Convolutional Neural Network (CNN) Face Detector in Dlib <http://dlib.net/cnn_face_detector.py.html>`_ is a deep learning-based approach for detecting
faces in images. Unlike traditional computer vision techniques that rely on hand-crafted features, CNNs learn to extract relevant features from the input
data, which makes them more effective in dealing with complex tasks like face detection. It achieved an accuracy of 97.6% on the LFW dataset. Additionally,
the model is robust to variations in lighting, pose, and expression, making it suitable for real-world applications.


Example:

.. code-block:: python

    from dronevis.models import CNNFaceDetection

    model = CNNFaceDetection()
    model.load_model()
    model.detect_webcam()


Dlib CNN Face Detection
-----------------------

.. autoclass:: dronevis.models.CNNFaceDetection
