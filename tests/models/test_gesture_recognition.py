"""Test gesture recongnition model"""
import pytest
import numpy as np
import cv2

from dronevis.models.gesture_recognition import GestureRecognition


@pytest.fixture
def model():
    """Model fixture"""
    gesture_model = GestureRecognition()
    gesture_model.load_model()
    yield gesture_model
    del gesture_model


@pytest.mark.parametrize(
    ["min_detection_confidence", "min_tracking_confidence"],
    [(0.5, 0.5)],
)
def test_model_init(min_detection_confidence, min_tracking_confidence):
    """Test model init"""
    gesture_model = GestureRecognition(
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )
    assert gesture_model.min_detection_confidence == min_detection_confidence
    assert gesture_model.min_tracking_confidence == min_tracking_confidence


@pytest.mark.parametrize(
    ["min_detection_confidence", "min_tracking_confidence"],
    [
        ("wrong", 0.5),
        (0.5, "wrong"),
        (1.2, 0.5),
        (1.2, -1.2),
    ],
)
def test_model_init_error(min_detection_confidence, min_tracking_confidence):
    """Test model init error"""
    with pytest.raises(AssertionError):
        GestureRecognition(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )


def test_model_load_error():
    """Test model prediction raises an error for
    not loading.
    """
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    model = GestureRecognition()
    with pytest.raises(AssertionError):
        model.predict(image)


def test_model_load(model):
    """Test model loading"""
    landmark_list = [[10, 20, 30], [20, 30, 40], [30, 40, 50]]
    pre_processed_landmark_list = model._pre_process_landmark(landmark_list)
    assert len(pre_processed_landmark_list) == 9
    assert model.keypoints_classifier is not None


def test_detect_webcam(monkeypatch, mocker):
    """Test webcam detection"""
    mocked = mocker.Mock()
    imshow_mock = mocker.Mock()
    mocked.read.return_value = True, np.zeros((100, 100, 3), dtype=np.uint8)
    monkeypatch.setattr(cv2, "VideoCapture", lambda x: mocked)
    monkeypatch.setattr(cv2, "imshow", imshow_mock)
    monkeypatch.setattr(cv2, "waitKey", lambda x: ord("q"))

    model = GestureRecognition()
    model.load_model()
    model.detect_webcam()
    args, _ = imshow_mock.call_args
    assert args[1].shape == (250, 250, 3)
    assert args[0].lower() == "Gesture Recognition".lower()
