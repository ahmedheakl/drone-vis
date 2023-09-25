"""Test action recognition model"""
import numpy as np

from dronevis.models.yolov5_torch import YOLOv5


def test_init():
    """Test initailization"""
    model = YOLOv5()
    assert model.net is None


def test_transform_image():
    """Test transform_img"""
    model = YOLOv5()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    processed_image = model.transform_img(image)
    assert np.equal(processed_image, image).all()
