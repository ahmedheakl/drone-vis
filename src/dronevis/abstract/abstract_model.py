from abc import ABC, abstractmethod


class CVModel(ABC):
    """Base class for creating custom comptervision models.
    To use the abstract class just inherit it, and override
    the abstract method.
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