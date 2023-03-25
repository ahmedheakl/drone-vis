"""Testing demo drone functionality"""
import time
import pytest

from dronevis.drone_connect import DemoDrone
from dronevis.utils.general import init_logger
from dronevis.models.mediapipe_face_detection import FaceDetectModel


@pytest.fixture
def setup_logger():
    init_logger(level="info")


def test_is_not_connected_when_initialized():
    """When the drone is initialized, its `is_connected` property
    should be set to False"""
    drone = DemoDrone()
    assert drone.is_connected == False


def test_ip_address_setting():
    """Provided IP address should be set for the drone"""
    ip_address = "1.1.1.1"
    drone = DemoDrone(ip_address)
    assert drone.ip_address == ip_address


@pytest.mark.parametrize("ip_address", [".0.0.0", "012.0.02.300", "256.0.0.0"])
def test_invalid_ip_address(ip_address: str):
    """Invalid IP addresses formats should be discarded, and the
    drone should raise a ValueError"""
    with pytest.raises(ValueError):
        DemoDrone(ip_address)


def test_video_thread_disconnet():
    """Video cannot be disconnected if it was not initialized"""
    drone = DemoDrone()
    with pytest.raises(ValueError):
        drone.disconnect_video()


def test_callback_should_be_callable():
    """Provided callback to the demo drone should be callable object"""
    drone = DemoDrone()
    with pytest.raises(TypeError):
        drone.set_callback("WRONG")  # type: ignore


def test_drone_is_connected():
    """When `connect` method is called, the `is_connected` property
    should be set to True"""
    drone = DemoDrone()
    drone.connect()
    assert drone.is_connected


@pytest.mark.parametrize(
    "control_name, control_method",
    [
        ("takeoff", DemoDrone().takeoff),
        ("land", DemoDrone().land),
        ("calibrate", DemoDrone().calibrate),
        ("forward", DemoDrone().forward),
        ("backward", DemoDrone().backward),
        ("left", DemoDrone().left),
        ("right", DemoDrone().right),
        ("up", DemoDrone().upward),
        ("down", DemoDrone().downward),
        ("rotating left", DemoDrone().rotate_left),
        ("rotating right", DemoDrone().rotate_right),
        ("hover", DemoDrone().hover),
    ],
)
def test_control_stdout(capsys, setup_logger, control_name, control_method):
    control_method()
    capture = capsys.readouterr()
    assert control_name in capture.err.lower()


def test_stop_connection(capsys, setup_logger):
    """Drone `is_connected` property should be set to `False` when
    the stop method is called"""
    drone = DemoDrone()
    drone.connect()
    assert drone.is_connected
    drone.stop()
    capture = capsys.readouterr()
    assert "drone disconnected" in capture.err.lower()
    assert drone.is_connected == False


# def test_stop_video_thread(capsys):
#     """Drone video thread should stop and set to None when the
#     method `stop` is called"""
#     init_logger("debug")
#     drone = DemoDrone()
#     model = FaceDetectModel()
#     model.load_model()
#     drone.connect_video(print, model)
#     assert drone.video_thread is not None
#     assert drone.video_thread.running
#     time.sleep(2)
#     drone.stop()
#     assert drone.video_thread is None
#     capture = capsys.readouterr()
#     assert "video thread stopped" in capture.err.lower()
