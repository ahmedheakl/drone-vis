from abc import ABC, abstractmethod

class CVModel(ABC):
    """Base class for creating custom comptervision models.
    
    To use the abstract class just inherit it, and override
    the abstract method.
    
    Main methods:
    
    1. ``load_model``
    Load model weights from web or cache. 
    You only need to download the model weights once,
    and they will be stored and loaded automatically each time you use them later.
        
    2. ``predict``
    Run model inference on input image
    You don't have to transform the image before the inference, input images will be transformed automatically.
        
    3. ``transform_img``
    Transform input image according to models transformations
        
    4. ``detect_webcam``
    Start webcam (or any camera) detection
    """

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def predict(self, image):
        pass

    @abstractmethod
    def transform_img(self, image):
        pass
    
    @abstractmethod
    def detect_webcam(self, video_index, window_name="Cam Detection"):
        pass