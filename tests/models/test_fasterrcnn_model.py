"""Test faset rcnn model"""
from dronevis.models.faster_rcnn_torch import FasterRCNN


def test_load_model():
    """Test model loading"""
    model = FasterRCNN()
    model.load_model()
    assert model.transform is not None
    assert model.net is not None
    assert not model.net.training
    assert str(model.net).startswith("FasterRCNN")
