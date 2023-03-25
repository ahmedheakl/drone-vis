"""Testing video thread base class"""
from typing import Generator
import pytest
import time

from dronevis.abstract.base_video_thread import BaseVideoThread
from dronevis.models.mediapipe_face_detection import FaceDetectModel

VIDEO_INDEX = "./test_video.avi"


@pytest.fixture(scope="session")
def vid_thread() -> Generator[BaseVideoThread, None, None]:
    """Fixture for initializing a thread with dummy model
    and callback"""
    BaseVideoThread._instances = {}
    closing_callback = lambda: None
    model = FaceDetectModel()
    model.load_model()
    thread = BaseVideoThread(closing_callback, model)
    thread.video_index = VIDEO_INDEX
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


@pytest.mark.parametrize(
    "callback, model",
    [
        ("WRONG", "WRONG"),
        ("WRONG", FaceDetectModel()),
        (lambda: 3, "WRONG"),
    ],
)
def test_initialize_thread_with_wrong_types(callback, model):
    """Thread class should catch and handle errors if user provided
    a wrong type of either a callback or a model.
    """
    BaseVideoThread._instances = {}
    with pytest.raises(TypeError):
        BaseVideoThread(callback, model)


def test_consecutive_threads():
    """When openning two threads consecutively, the second one
    should not get stuck.
    """
    closing_callback = lambda: None
    model = FaceDetectModel()
    model.load_model()
    thread1 = BaseVideoThread(closing_callback, model, video_index=VIDEO_INDEX)
    thread1.video_index = VIDEO_INDEX
    thread1.show_window = False
    thread1.resume()
    time.sleep(2)
    thread1.stop()
    time.sleep(0.1)

    closing_callback = lambda: None
    model = FaceDetectModel()
    model.load_model()
    thread2 = BaseVideoThread(closing_callback, model)
    assert thread2.running == False
    thread2.video_index = VIDEO_INDEX
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
    assert vid_thread.running == False
