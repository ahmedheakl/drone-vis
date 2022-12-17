.. currentmodule:: dronevis

Detection Algorithms
====================

Detection algorithms are the most frequenlty used in computer vision alogrithms generally, and in drones navigation specifically.
Henceforth, the library comes in equipped with **state-of-the-art (SOTA) algorithms** along with different implementations: 

.. _detectionimplement:

- `Faster Region-based CNN (R-CNN) <https://arxiv.org/abs/1506.01497>`_ (PyTorch)
- `CenterNet <https://arxiv.org/abs/1904.08189>`_ (Mxnet)
- `You Only Look Once (YOLO) <https://arxiv.org/abs/1506.02640>`_ (Mxnet)
- `Signle-Shot Detector (SSD) <https://arxiv.org/abs/1512.02325>`_ (PyTorch, Mxnet)

Detection on Your Web Camera
----------------------------

You can get started by feeding a video stream from your web camera **(or any camera)** with a few lines of code. 

.. code-block:: python

    from dronevis.detection_torch import FasterRCNN

    model = FasterRCNN()    # initialize model instance 
    model.load_model()      # load the model weights  
    model.detect_webcam()   # start video detection

A window pops-up with your webcam video stream, and boxes around detected objects. 

.. note:: 

    The model weights need to be downloaded, so make sure you have a working internet connection.
    However, once the weights are downloaded once, they will be stored in ``~/.cache/torch/hub/checkpoints`` (on Ubuntu) and you needn't to download them again.

You can see that the models run with ``PyTorch``, which will automatically check whether you have a GPU device and load the model accordingly.
If you have multiple GPUs and you want to specify one of them for the detection, just set the device property of the model to your desired choice (either ``"cuda:<device-index>"`` or ``"cpu"``):

.. code-block:: python
    
    model.device = "cuda:1" # set second GPU (index=1) for inference

Different Model Implementations
---------------------------------

The library takes into account the numerous implementations found on the internet, and that users usually prefer a framework over the other. Hence, detection models are **currenly** built with two frameworks: 

- PyTorch 
- Mxnet

You can see the :ref:`types of implementation <detectionimplement>`.
However, for easier user interactivity, major used methods are unified across all models.
Each model has 4 main methods:

- ``load_model`` : load the model weights from cache, or download them. 
- ``predict``   : run the model on input image 
- ``transform_img`` : run the model's transformation on input image
- ``detect_webcam`` : start detection on your webcam.


Abstract Models
---------------

To provide a unified interface for all detection models, all implementations must inherit from an abstract base class. 

Main Abstract Model
~~~~~~~~~~~~~~~~~~~

.. autoclass:: dronevis.abstract.abstract_model.CVModel

Now, each model inherits from this abstract class, and **must implement its abstract methods**.
You can implement your own model as follows:  

.. code-block:: python

    from drone.abstract import CVModel
    
    class CustomModel(CVModel):

        def load_model(self):
            """Load your model weights""""
            pass

        def predict(self, image):
            """Run model on input image and return inference results""""
            pass
        
        def transform_img(self, image):
            """Transform input image""""
            pass
        
        def detect_webcam(self, video_index, window_name):
            """Retrieve video stream from device at video index, and start model inference""""
            pass

Torch Abstract Models
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: dronevis.abstract.abstract_torch_model.TorchDetectionModel


As pretrained PyTorch models have many methods into common, ``TorchDetectionModel`` unifies the common methods in a single class, and each torch model implementation inherits from this class. 
However, each inherited model must implement the ``load_model`` method. 

.. code-block:: python
    :emphasize-lines: 8, 9, 10
    
    from dronevis.abstract.abstract_torch_model import TorchDetectionModel
    
    class CustomTorchModel(TorchDetectionModel):
        
        def __init__(self): 
            super(CustomTorchModel, self).__init__()

        def load_model(self):
            """Load model weights"""
            pass

Mxnet Abstract Models
~~~~~~~~~~~~~~~~~~~~~

Since `GluonCV <https://cv.gluon.ai/>`_ has an enormous support for mxnet, we implemented mxnet models with gluoncv models.

.. autoclass:: dronevis.abstract.abstract_gluoncv_model.GluonCVModel

As pretrained Mxnet models have many methods into common, ``GluonCVModel`` unifies the common methods in a single class, and each mxnet model implementation inherits from this class. 
However, each inherited model must implement the ``transform_img`` and ``load_and_transform_img`` methods.


    
.. code-block:: python
    :emphasize-lines: 12-23, 24-34
    
    from dronevis.abstract.abstract_gluoncv_model import GluonCVModel
    
    class CustomMxnetModel(GluonCVModel):
        
        def __init__(self): 
            super(CustomTorchModel, self).__init__(model_name="mxnet_model")

        def load_model(self, model_path) -> None:
            print("Loading mxnet model ...")
            super().load_model(model_path=model_path)

        def transform_img(self, img: np.ndarray):
            """Transform the input image to have a short side size of 512

            Args:
                img (np.ndarray): input image

            Returns:
                Tuple[mxnet.NDArray, np.ndarray]: A (1, 3, H, W) mxnet NDArray as input
                    to network, and a numpy ndarray as original un-normalized color
                    image for display
            """
            pass

        def load_and_transform_img(self, img_path):
            """Load img from harddisk

            Args:
                img_path (str): path of the img on disk

            Returns:
                (mx.NDArray, np.ndarray): input-ready image for inference,
                    original image non-normalized
            """
            pass
    