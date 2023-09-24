"""Testing video thread base class"""
from typing import Generator
import time
import os
import pytest

from dronevis.abstract.base_video_thread import BaseVideoThread

TEST_DATA_PATH = os.getenv("TEST_DATA_PATH", "")
VIDEO_PATH = TEST_DATA_PATH + "/test_video.avi"


class DummyTest:
    """Dummy class for testing"""


@pytest.fixture(scope="session")
def vid_thread() -> Generator[BaseVideoThread, None, None]:
    """Fixture for initializing a thread with dummy model
    and callback"""
    BaseVideoThread._instances = {}
    closing_callback = lambda: None
    operating_callback = lambda: None
    thread = BaseVideoThread(closing_callback, operating_callback, "Face")
    thread.video_index = VIDEO_PATH
    yield thread


@pytest.fixture(scope="session", autouse=True)
def close_video_thread(vid_thread: BaseVideoThread):
    """Close the opened thread and remove its instance after
    all tests in this scope are finished.
    """
    yield
    vid_thread.close_thread()
    vid_thread.join()
    BaseVideoThread._instances = {}


def test_initialize_thread_with_wrong_types():
    """Thread class should catch and handle errors if user provided
    a wrong type of either a callback or a model.
    """
    BaseVideoThread._instances = {}
    with pytest.raises(TypeError):
        BaseVideoThread("Wrong", "Wrong", "Face")


def test_initialize_thread_with_wrong_model():
    """Thread class should catch and handle errors if user provided
    a wrong model name.
    """
    BaseVideoThread._instances = {}
    with pytest.raises(ValueError):
        BaseVideoThread(lambda: None, lambda: None, "Wrong")


def test_change_model_with_wrong_type():
    """When chaning the model for the video thread, the new model
    should be an instance of `CVModel` otherwise the video thread
    should raise an error.
    """
    BaseVideoThread._instances = {}
    closing_callback = lambda: None
    thread = BaseVideoThread(
        closing_callback,
        closing_callback,
        "Face",
    )
    with pytest.raises(ValueError):
        thread.change_model("Wrong")  # type: ignore


def test_consecutive_threads():
    """When openning two threads consecutively, the second one
    should not get stuck.
    """
    closing_callback = lambda: None
    thread1 = BaseVideoThread(closing_callback, closing_callback, "Face")
    thread1.video_index = VIDEO_PATH
    assert thread1.video_index == VIDEO_PATH
    thread1.show_window = False
    assert not thread1.show_window
    thread1.resume()
    time.sleep(2)
    thread1.stop()
    time.sleep(0.1)

    closing_callback = lambda: None
    thread2 = BaseVideoThread(closing_callback, closing_callback, "Face")
    assert not thread2.running
    thread2.video_index = VIDEO_PATH
    thread2.show_window = False
    thread2.resume()
    time.sleep(2)
    thread2.stop()
    thread2.close_thread()
    thread2.join()


def test_running_is_equal_true(vid_thread: BaseVideoThread):
    """Thread attribute `running` should be set to true when
    the thread is initialized.
    """
    vid_thread.resume()
    assert vid_thread.running
    vid_thread.stop()
    assert not vid_thread.running
