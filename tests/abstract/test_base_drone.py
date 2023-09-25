"""Testing base class for drone"""
from typing import Generator
import pytest
from dronevis.abstract.base_drone import BaseDrone


@pytest.fixture
def drone() -> Generator[BaseDrone, None, None]:
    """Fixture for initializing a drone"""
    drone = BaseDrone()
    yield drone
    drone.stop()


def test_is_connected_for_initialized_models():
    """When the drone is initialized, its `is_connected`
    property should be set to False"""
    drone = BaseDrone()
    assert not drone.is_connected


@pytest.mark.parametrize(
    "closing_callback, operating_callback, model_name",
    [
        ("WRONG", "WRONG", "None"),
        ("WRONG", lambda x: 3, "None"),
    ],
)
def test_connect_video_callbacks(
    drone: BaseDrone,
    closing_callback,
    operating_callback,
    model_name,
):
    """When the drone is provided with a bad formatted callback"""
    with pytest.raises(TypeError):
        drone.connect_video(closing_callback, operating_callback, model_name)


def test_connect_video_model_name_arg():
    """When the drone is provided with a bad formatted callback"""
    with pytest.raises(ValueError):
        BaseDrone().connect_video(lambda x: 3, lambda x: 3, "WRONG")


@pytest.mark.parametrize("ip_address", [".0.0.0", "012.0.02.300", "256.0.0.0"])
def test_wrong_ip_address_format(ip_address: str):
    """When the drone is provided with a bad formatted ip_address
    it should raise a value error"""
    with pytest.raises(ValueError):
        BaseDrone(ip_address)


@pytest.mark.parametrize(
    "control_method",
    [
        BaseDrone().takeoff,
        BaseDrone().land,
        BaseDrone().calibrate,
        BaseDrone().forward,
        BaseDrone().backward,
        BaseDrone().left,
        BaseDrone().right,
        BaseDrone().upward,
        BaseDrone().downward,
        BaseDrone().rotate_left,
        BaseDrone().rotate_right,
        BaseDrone().hover,
        BaseDrone().emergency,
        BaseDrone().reset,
        BaseDrone().set_config,
    ],
)
def test_control_method_return_true(control_method):
    """When calling a control method, it should return True"""
    assert control_method()
