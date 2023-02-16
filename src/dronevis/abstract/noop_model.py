from dronevis.abstract import CVModel

class NOOPModel(CVModel):
    
    def __init__(self) -> None:
        pass
        
    def load_model(self):
        pass
    
    def transform_img(self, image):
        return image
    
    def predict(self, image):
        return image
    
    def detect_webcam(self, video_index, window_name="Cam Detection"):
        pass