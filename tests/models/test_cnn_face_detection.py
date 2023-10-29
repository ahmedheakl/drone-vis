"""Test cnn face detection model."""
import pytest
import numpy as np
import cv2

from dronevis.models import CNNFaceDetection


def test_init():
    """Test initailization"""
    model = CNNFaceDetection()
    assert model.net is None


def test_load_model():
    """Test model loading"""
    model = CNNFaceDetection()
    model.load_model()
    assert model.net


def test_transform_image():
    """Test transform_img"""
    model = CNNFaceDetection()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    processed_image = model.transform_img(image)
    assert processed_image.shape == image.shape[:-1]


def test_predict():
    """Test predict"""
    model = CNNFaceDetection()
    model.load_model()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    prediction = model.predict(image)
    assert prediction.shape == (200, 200, 3)


def test_predict_with_unloaded_model():
    """Test predict with unloaded model"""
    model = CNNFaceDetection()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    assert model.net is None
    prediction = model.predict(image)
    assert model.net
    assert prediction.shape == (200, 200, 3)


def test_detect_webcam(monkeypatch: pytest.MonkeyPatch, mocker):
    """Test webcam detection"""
    mocked = mocker.Mock()
    imshow_mock = mocker.Mock()
    mocked.read.return_value = True, np.zeros((100, 100, 3), dtype=np.uint8)
    monkeypatch.setattr(cv2, "VideoCapture", lambda x: mocked)
    monkeypatch.setattr(cv2, "imshow", imshow_mock)
    monkeypatch.setattr(cv2, "waitKey", lambda x: ord("q"))

    model = CNNFaceDetection()
    model.load_model()
    model.detect_webcam()
    args, _ = imshow_mock.call_args
    assert args[1].shape == (100, 100, 3)
    assert args[0].lower() == "cnn face detection".lower()

    monkeypatch.setattr(mocked, "isOpened", lambda: False)
    model.detect_webcam()
    assert imshow_mock.call_count == 1
