"""Testing video thread base class"""
import pytest
import time

from dronevis.abstract.base_video_thread import BaseVideoThread
from dronevis.models.mediapipe_face_detection import FaceDetectModel

VIDEO_INDEX = "./test_video.avi"


@pytest.fixture
def thread() -> BaseVideoThread:
    """Fixture for initializing a thread with dummy model
    and callback"""
    closing_callback = lambda: None
    model = FaceDetectModel()
    model.load_model()
    thread = BaseVideoThread(closing_callback, model)
    thread.video_index = VIDEO_INDEX
    return thread


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
    a wrong type of either a callback or a model"""
    with pytest.raises(TypeError):
        BaseVideoThread(callback, model)


def test_running_is_equal_true(thread):
    """Thread attribute `running` should be set to true when
    the thread is initialized"""
    assert thread.running
    thread.stop()
    assert thread.running == False


def test_change_model_with_wrong_type(thread):
    """Thread should catch and handle an error when it is asked
    to change the model with a wrong type"""
    with pytest.raises(TypeError):
        thread.change_model(BaseVideoThread)


def test_consecutive_threads():
    """When openning two threads consecutively, the second one
    should not get stuck"""
    closing_callback = lambda: None
    model = FaceDetectModel()
    model.load_model()
    thread = BaseVideoThread(closing_callback, model, video_index=VIDEO_INDEX)
    thread.video_index = VIDEO_INDEX
    thread.resume()
    time.sleep(2)
    thread.stop()
    time.sleep(0.1)

    closing_callback = lambda: None
    model = FaceDetectModel()
    model.load_model()
    thread = BaseVideoThread(closing_callback, model)
    thread.video_index = VIDEO_INDEX
    thread.resume()
    time.sleep(2)
    thread.stop()
