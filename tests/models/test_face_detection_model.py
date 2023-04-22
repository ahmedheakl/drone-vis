"""Test face detection model"""
import pytest
import numpy as np

from dronevis.models.face_detection import FaceDetectModel


def test_face_detect_model_init():
    """Test model initialization"""
    with pytest.raises(TypeError):
        FaceDetectModel(confidence="0.6")

    with pytest.raises(AssertionError):
        FaceDetectModel(confidence=-1)


def test_face_detect_model_predict():
    """Test model prediction"""
    f_detect = FaceDetectModel()
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img_out = f_detect.predict(img)
    assert img_out.shape == img.shape
