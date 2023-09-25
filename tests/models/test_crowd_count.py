"""Test action recognition model"""
import pytest
import numpy as np
import cv2
from ezcrowdcount import IMG_SIZE

from dronevis.models import CrowdCounter


def test_init():
    """Test initailization"""
    model = CrowdCounter()
    assert model.net is None


def test_load_model():
    """Test model loading"""
    model = CrowdCounter()
    model.load_model()
    assert model.net is not None
    assert model.net.training is False


def test_transform_image():
    """Test transform_img"""
    model = CrowdCounter()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    image = model.transform_img(image)
    assert image.shape == (1, 1, *IMG_SIZE)


def test_predict():
    """Test predict"""
    model = CrowdCounter()
    model.load_model()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    prediction = model.predict(image)
    assert prediction.shape == (1, 1, *IMG_SIZE)
    et_count = int(np.sum(prediction))
    assert et_count == 0


def test_predict_with_unloaded_model():
    """Test predict with unloaded model"""
    model = CrowdCounter()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    assert model.net is None
    prediction = model.predict(image)
    assert model.net
    assert prediction.shape == (1, 1, *IMG_SIZE)
    et_count = int(np.sum(prediction))
    assert et_count == 0


def test_detect_webcam(monkeypatch: pytest.MonkeyPatch, mocker):
    """Test webcam detection"""
    mocked = mocker.Mock()
    imshow_mock = mocker.Mock()
    mocked.read.return_value = True, np.zeros((100, 100, 3), dtype=np.uint8)
    monkeypatch.setattr(cv2, "VideoCapture", lambda x: mocked)
    monkeypatch.setattr(cv2, "imshow", imshow_mock)
    monkeypatch.setattr(cv2, "waitKey", lambda x: ord("q"))

    model = CrowdCounter()
    model.load_model()
    model.detect_webcam()
    args, _ = imshow_mock.call_args
    assert args[1].shape == (*IMG_SIZE, 3)
    assert args[0].lower() == "Crowd Counter".lower()

    monkeypatch.setattr(mocked, "isOpened", lambda: False)
    model.detect_webcam()
    assert imshow_mock.call_count == 1

    monkeypatch.setattr(mocked, "isOpened", lambda: True)
    mocked.read.return_value = False, None
    model.detect_webcam()
    assert imshow_mock.call_count == 1
