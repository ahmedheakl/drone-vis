"""Testing demo drone functionality"""
import time
import os
import pytest

from dronevis.drone_connect import DemoDrone
from dronevis.drone_connect.demo_drone import DemoVideoThread, DemoNavThread
from dronevis.utils.general import init_logger
from dronevis.models.mediapipe_face_detection import FaceDetectModel

TEST_DATA_PATH = os.getenv("TEST_DATA_PATH", "")
TEST_VIDEO = TEST_DATA_PATH + "/test_video.avi"


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
        ("emergency", DemoDrone().emergency),
        ("reseting", DemoDrone().reset),
        ("", DemoDrone().set_config),
    ],
)
def test_control_stdout(capsys, setup_logger, control_name, control_method):
    assert control_method()
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


def test_video_thread_should_not_close_when_disconnect_video() -> None:
    """When disconnecting video thread, it should not fully close, i.e. `is_stopped`
    property should be still set to False. And hence allowing other threads to be openned
    during the execution of the program.
    """
    closing_callback = lambda: None
    DemoVideoThread._instances = {}
    model = FaceDetectModel()
    model.load_model()
    _ = DemoVideoThread(closing_callback, model, video_index=TEST_VIDEO)
    drone = DemoDrone()
    drone.connect_video(closing_callback, model)
    assert drone.video_thread is not None
    assert drone.video_thread.running

    drone.disconnect_video()
    assert drone.video_thread is not None
    assert drone.video_thread.is_stopped == False
    assert drone.video_thread.running == False


def test_stop_video_thread(capsys):
    """Drone video thread should stop and set to None when the
    method `stop` is called.
    """
    init_logger("debug")
    drone = DemoDrone()
    model = FaceDetectModel()
    model.load_model()
    drone.connect_video(print, model)
    assert drone.video_thread is not None
    assert drone.video_thread.running
    time.sleep(2)
    drone.stop()
    assert drone.video_thread is None
    capture = capsys.readouterr()
    assert "video thread stopped" in capture.err.lower()


def test_default_callback():
    """If no callback is provided, the thread should have
    its own callback, i.e. print method.
    """
    drone = DemoDrone()
    drone.set_callback()
    assert drone.nav_thread is not None
    assert drone.nav_thread.running
    assert drone.nav_thread.callback == drone._print_navdata
    drone.stop()
    del drone


def test_set_callback():
    """When the drone receives a callback for the nav thread,
    it should initialized it if it wasn't initialized. It also
    should set the provided callback as a callback for nav thread
    """
    drone = DemoDrone()
    callback = lambda navdata: None
    drone.set_callback(callback)
    assert drone.nav_thread is not None
    assert drone.nav_thread.callback == callback
    assert drone.nav_thread.running
    another_callback = lambda navdata: print(navdata)
    drone.set_callback(another_callback)
    assert drone.nav_thread is not None
    assert drone.nav_thread.callback == another_callback
    assert drone.nav_thread.running
    drone.stop()
    assert drone.nav_thread is None


def test_set_non_callable_method_for_nav_thread():
    """When the nav thread is provided with a non-callable method,
    it should raise a type error.
    """
    callback = lambda navdata: None
    thread = DemoNavThread(callback)
    another_callback = lambda navdata: print(navdata)
    thread.change_callback(another_callback)
    assert thread.callback == another_callback
    with pytest.raises(TypeError):
        thread.change_callback("WRONG")  # type: ignore
    thread.stop()
