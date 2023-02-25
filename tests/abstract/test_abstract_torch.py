"""Testing detection with torch models abstract class"""
import pytest
import numpy as np

from dronevis.abstract.abstract_torch_model import TorchDetectionModel
from dronevis.detection_torch import SSD


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
