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


@pytest.mark.parametrize("ip_address", [".0.0.0", "012.0.02.300", "256.0.0.0"])
def test_wrong_ip_address_format(ip_address: str):
    """When the drone is provided with a bad formatted ip_address
    it should raise a value error"""
    with pytest.raises(ValueError):
        BaseDrone(ip_address)
