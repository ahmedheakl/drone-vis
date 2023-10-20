HOG Face Detection
==================

`The Histogram of Oriented Gradients (HOG) <https://www.researchgate.net/publication/342886529_Face_Detection_Histogram_of_Oriented_Gradients_and_Bag_of_Feature_Method>`_ classifier is another
popular face detection algorithm that has shown excellent performance in various computer vision applications. Proposed by Dalal and Triggs, HOG is based on the idea of using the distribution
of gradient orientation in small cells to represent the features of an image. The algorithm first extracts the gradient orientation histograms from the input image and then uses a sliding window
approach to detect potential face regions. The HOG classifier has several advantages over the Haar classifier. Firstly, it is more robust to variations in lighting and pose, as it uses a
distribution of gradient orientations rather than a single orientation. Secondly, it is less sensitive to the size of the face, allowing it to detect faces of varying sizes. Finally, the HOG
classifier is computationally more efficient than the Haar classifier, making it a better choice for real-time applications. Evaluated on "Labeled Faces in the Wild" (LFW) dataset, it achieved
an accuracy of 95.6\% with a false positive rate of 0.13. However, the HOG classifier also has some limitations. It requires a large amount of training data to achieve good performance, and the
training process can be computationally expensive. Additionally, the classifier is sensitive to the choice of parameters, such as the size of the cells and the number of bins used in the histogram.

Example:

.. code-block:: python

    from dronevis.models import HOGFaceDetection

    model = HOGFaceDetection() # create model instance
    model.load()                # load model weights
    model.detect_webcam()       # run camera detection


HOG Face Detection Class
-------------------------

.. autoclass:: dronevis.models.HOGFaceDetection