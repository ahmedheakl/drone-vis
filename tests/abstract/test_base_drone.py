"""Testing base class for drone"""
import pytest
from dronevis.abstract.base_drone import BaseDrone


@pytest.fixture
def drone() -> BaseDrone:
    return BaseDrone()


def test_is_connected_for_initialized_models():
    """When the drone is initialized, its `is_connected`
    property should be set to False"""
    drone = BaseDrone()
    assert drone.is_connected == False


@pytest.mark.parametrize(
    "callback, model",
    [
        ("WRONG", "WRONG"),
        (lambda x: 3, "WRONG"),
        ("WRONG", BaseDrone),
    ],
)
def test_connect_video_args(drone, callback, model):
    with pytest.raises(TypeError):
        drone.connect_video(callback, model)
