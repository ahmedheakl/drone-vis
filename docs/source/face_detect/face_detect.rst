Face Detection
==============

This module load and inference images for face detection. 

Example: 

.. code-block:: python

    from dronevis.models import FaceDetectModel
    
    model = FaceDetectModel()    # create model instance
    model.load_model()           # load model weights 
    model.detect_webcam()        # run camera detection


Face Detection Class
--------------------


.. autoclass:: dronevis.models.FaceDetectModel