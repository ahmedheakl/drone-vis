from abc import ABC, abstractmethod

class CVModel(ABC):
    @abstractmethod 
    def predict(self, img, img_data=None):
        pass
    
    @abstractmethod
    def load_model(self, model_path):
        pass
    
    @abstractmethod
    def transform_img(self, img):
        pass
    