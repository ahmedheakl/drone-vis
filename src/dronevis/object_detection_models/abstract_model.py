from abc import ABC, abstractmethod


class CVModel(ABC):
    """Base class for creating custom comptervision models.
    To use the abstract class just inherit it, and override
    the abstract method.
    """

    @abstractmethod
    def load_model(self, model_path):
        pass

    @abstractmethod
    def predict(self, img, img_data=None):
        pass

    @abstractmethod
    def transform_img(self, img):
        pass
