import pytest
from dronevis.detection_torch import SSD
import numpy as np

@pytest.fixture
def load_model_instance():
    return SSD()

@pytest.fixture
def load_model_weights(load_model_instance):
    load_model_instance.load_model()
    return load_model_instance

@pytest.fixture
def load_dummy_data():
    return np.zeros((10, 10), dtype=np.float32)

@pytest.mark.parametrize("threshold", [0.2, 2, -2])
def test_prediction_raises(threshold, load_model_instance, load_dummy_data):
    with pytest.raises(AssertionError) as exc_info:
        load_model_instance.predict(load_dummy_data, detection_threshold=threshold)
        
@pytest.mark.parametrize("threshold", [-2, 2])
def test_load_model_with_weights(threshold, load_model_weights, load_dummy_data):
    with pytest.raises(AssertionError) as exc_info:
        load_model_weights.predict(load_dummy_data, detection_threshold=threshold)
    