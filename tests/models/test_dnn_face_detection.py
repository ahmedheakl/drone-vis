"""Test dnn face detection model."""
import os

import pytest
import numpy as np
import cv2
from PIL import Image

from dronevis.models import DNNFaceDetection

TEST_DATA_PATH = os.getenv("TEST_DATA_PATH", "")
TEST_PHOTO = TEST_DATA_PATH + "/human_face.png"


def test_init():
    """Test initailization"""
    model = DNNFaceDetection()
    assert model.net is None


def test_bad_confidence_score():
    """Test bad confidence score"""
    model = DNNFaceDetection(confidence="wrong")
    assert model.confidence == 0.5

    model = DNNFaceDetection(confidence=1.5)
    assert model.confidence == 0.5


def test_load_model():
    """Test model loading"""
    model = DNNFaceDetection()
    model.load_model()
    assert model.net


def test_bad_load():
    """Test bad model loading"""
    model = DNNFaceDetection()
    with pytest.raises(ValueError):
        model.load_model(model_name="wrong")


def test_load_tf_model():
    """Test loading tensorflow model"""
    model = DNNFaceDetection()
    model.load_model(model_name="tf")
    assert model.net


def test_transform_image():
    """Test transform_img"""
    model = DNNFaceDetection()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    processed_image = model.transform_img(image)
    assert processed_image.shape == image.shape


def test_predict():
    """Test predict"""
    model = DNNFaceDetection()
    model.load_model()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    prediction = model.predict(image)
    assert prediction.shape == (200, 200, 3)


def test_predict_with_existing_faces():
    """Test predict with existing faces"""
    model = DNNFaceDetection()
    model.load_model()
    image = np.array(Image.open(TEST_PHOTO).convert("RGB"), dtype=np.uint8)
    prediction = model.predict(image)
    assert prediction.shape == image.shape


def test_predict_with_unloaded_model():
    """Test predict with unloaded model"""
    model = DNNFaceDetection()
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

    model = DNNFaceDetection()
    model.load_model()
    model.detect_webcam()
    args, _ = imshow_mock.call_args
    assert args[1].shape == (100, 100, 3)
    assert args[0].lower() == "dnn face detection".lower()

    monkeypatch.setattr(mocked, "isOpened", lambda: False)
    model.detect_webcam()
    assert imshow_mock.call_count == 1
