"""Test action recognition model"""
from typing import Literal
import pytest
import numpy as np
import cv2
import torch

from dronevis.models import ActionRecognizer


def test_init():
    """Test initailization"""
    model = ActionRecognizer()
    assert model.num_preds == 1
    assert model.net is None
    assert model.image_processor is None


@pytest.mark.parametrize(
    "model_name",
    ["google", "mcg", "facebook"],
)
def test_load_model(model_name: Literal["google", "mcg", "facebook"]):
    """Test model loading"""
    model = ActionRecognizer()
    model.load_model(model_name)
    assert model.net is not None
    assert model.image_processor is not None


def test_load_with_invalid_model_name():
    """Test model loading error"""
    model = ActionRecognizer()
    with pytest.raises(ValueError):
        model.load_model("wrong")


def test_transform_image_error():
    """Test transform_img error"""
    model = ActionRecognizer()
    image = np.zeros((200, 200, 3), dtype=np.uint8)

    processed_image = model.transform_img(image)
    assert np.equal(processed_image, image).all()


def test_transform_image():
    """Test transform_img"""
    model = ActionRecognizer()
    video = np.zeros((16, 200, 200, 3), dtype=np.uint8)

    model.load_model()
    processed_image: torch.Tensor = model.transform_img(video)
    assert processed_image != video


def test_detect_webcam(monkeypatch: pytest.MonkeyPatch, mocker):
    """Test webcam detection"""
    mocked = mocker.Mock()
    imshow_mock = mocker.Mock()
    mocked.read.return_value = True, np.zeros((100, 100, 3), dtype=np.uint8)
    monkeypatch.setattr(cv2, "VideoCapture", lambda x: mocked)
    monkeypatch.setattr(cv2, "imshow", imshow_mock)
    monkeypatch.setattr(cv2, "waitKey", lambda x: ord("q"))

    model = ActionRecognizer()
    model.load_model()
    model.detect_webcam()
    args, _ = imshow_mock.call_args
    assert args[1].shape == (100, 100, 3)
    assert args[0].lower() == "Action Recognition".lower()


def test_prediction():
    """Test model prediction"""
    model = ActionRecognizer()
    model.load_model()
    image = np.ones((16, 200, 200, 3), dtype=np.uint8)
    prediction = model.predict(image)
    assert prediction == "dancing ballet"  # a bit weird but it works


def test_prediction_with_unloaded_model():
    """Test model prediction raises an error for
    not loading.
    """
    image = np.zeros((16, 200, 200, 3), dtype=np.uint8)
    model = ActionRecognizer()
    assert model.net is None
    prediction = model.predict(image)
    assert model.net
    assert prediction == "dancing ballet"  # a bit weird but it works
