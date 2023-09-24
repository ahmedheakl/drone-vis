"""Model Factory Implementation"""
from dronevis.models import models_list


# pylint: disable=too-few-public-methods
class ModelFactory:
    """Factory class for creating models"""

    models_list = models_list

    @staticmethod
    def create_model(model_name: str):
        """Get model from model name"""
        if model_name not in models_list:
            raise ValueError(f"Model {model_name} is not supported")
        model_class = models_list[model_name]
        if model_name == "Segment":
            model = model_class(is_seg=True)  # type: ignore

        elif model_name == "Pose+Segment":
            model = model_class(is_seg_pose=True)
        elif model_name == "YOLOv8Track":
            model = model_class(track=True)
        else:
            model = model_class()

        if "Action" in model_name:
            model_type = model_name.split("Action")[1].lower()
            model.load_model(model_type)
        else:
            model.load_model()
        return model
