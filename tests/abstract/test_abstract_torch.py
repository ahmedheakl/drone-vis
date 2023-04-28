"""Testing detection with torch models abstract class"""
import pytest
import numpy as np
import torch

from dronevis.abstract.abstract_torch_model import TorchDetectionModel, cv2
from dronevis.models import SSD


@pytest.fixture
def load_model_instance() -> TorchDetectionModel:
    """Retrieving a model instance"""
    return SSD()


@pytest.fixture
def load_model_weights(load_model_instance: TorchDetectionModel) -> TorchDetectionModel:
    """Loading model weights for provided model"""
    load_model_instance.load_model()
    return load_model_instance


@pytest.fixture
def load_dummy_data() -> np.ndarray:
    """Loading some dummy data for model inference"""
    return np.zeros((10, 10), dtype=np.float32)


@pytest.mark.parametrize("threshold", [0.2, 2, -2])
def test_prediction_raises(
    threshold: float,
    load_model_instance: TorchDetectionModel,
    load_dummy_data: np.ndarray,
) -> None:
    """Testing that the model raises an assertion"""
    with pytest.raises(AssertionError) as _:
        load_model_instance.predict(load_dummy_data, detection_threshold=threshold)


@pytest.mark.parametrize("threshold", [-2, 2])
def test_load_model_with_weights(threshold, load_model_weights, load_dummy_data):
    with pytest.raises(AssertionError) as _:
        load_model_weights.predict(load_dummy_data, detection_threshold=threshold)


@pytest.fixture
def model():
    ssd_model = SSD()
    ssd_model.load_model()
    yield ssd_model
    del ssd_model


def test_detect_webcam(model, mocker, monkeypatch):
    mocked = mocker.Mock()
    imshow_mock = mocker.Mock()
    mocked.read.return_value = True, np.zeros((100, 100, 3), dtype=np.uint8)
    monkeypatch.setattr(cv2, "VideoCapture", lambda x: mocked)
    monkeypatch.setattr(cv2, "imshow", imshow_mock)
    monkeypatch.setattr(cv2, "waitKey", lambda x: ord("q"))

    model.detect_webcam()
    args, _ = imshow_mock.call_args
    assert args[1].shape == (100, 100, 3)
    assert args[0].lower() == "Cam Detection".lower()


def test_draw_boxes(model):
    """Test drawing boxes"""
    img = np.zeros((224, 224, 3), dtype=np.uint8)
    boxes = np.array([[0, 0, 50, 50], [100, 100, 150, 150]])
    classes = ["cat", "dog"]
    labels = torch.tensor([0, 1]).to(dtype=torch.int32)
    res = model.draw_boxes(boxes, classes, labels, img)
    assert isinstance(res, np.ndarray)
