"""Test action recognition model"""
import pytest
import numpy as np
import cv2

from dronevis.models import YOLOv8Detection, YOLOv8Pose, YOLOv8Segmentation


@pytest.mark.parametrize(
    "track",
    [True, False],
)
def test_init_detection(track: bool):
    """Test initailization"""
    model = YOLOv8Detection(track)
    assert model.net is None
    assert model.track == track


@pytest.mark.parametrize(
    "track",
    [True, False],
)
def test_init_pose(track: bool):
    """Test initailization"""
    model = YOLOv8Pose(track)
    assert model.net is None
    assert model.track == track


@pytest.mark.parametrize(
    "track",
    [True, False],
)
def test_init_segmentation(track: bool):
    """Test initailization"""
    model = YOLOv8Segmentation(track)
    assert model.net is None
    assert model.track == track


def test_load_detection():
    """Test model loading"""
    model = YOLOv8Detection()
    model.load_model()
    assert model.net


def test_load_pose():
    """Test model loading"""
    model = YOLOv8Pose()
    model.load_model()
    assert model.net


def test_load_segmentation():
    """Test model loading"""
    model = YOLOv8Segmentation()
    model.load_model()
    assert model.net


def test_predict_pose():
    """Test predict"""
    model = YOLOv8Pose()
    model.load_model()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    prediction = model.predict(image)
    assert prediction.shape == (200, 200, 3)


def test_predict_detection():
    """Test predict"""
    model = YOLOv8Detection()
    model.load_model()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    prediction = model.predict(image)
    assert prediction.shape == (200, 200, 3)


def test_predict_segmentation():
    """Test predict"""
    model = YOLOv8Segmentation()
    model.load_model()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    prediction = model.predict(image)
    assert prediction.shape == (200, 200, 3)


def test_predict_detection_track(mocker):
    """Test predict"""
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    model = YOLOv8Detection(track=True)
    net_mocker = mocker.Mock()
    results_mocker = mocker.Mock()
    results_mocker.plot = lambda: image
    net_mocker.track = mocker.Mock(return_value=[results_mocker])
    model.net = net_mocker

    prediction = model.predict(image)
    assert prediction.shape == (200, 200, 3)
    assert model.net.track.call_count == 1


def test_predict_with_unloaded_model():
    """Test predict with unloaded model"""
    model = YOLOv8Pose()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    assert model.net is None
    prediction = model.predict(image)
    assert model.net
    assert prediction.shape == (200, 200, 3)


def test_transform_image():
    """Test transform_img"""
    model = YOLOv8Pose()
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    processed_image = model.transform_img(image)
    assert np.equal(processed_image, image).all()


def test_detect_webcam(monkeypatch: pytest.MonkeyPatch, mocker):
    """Test webcam detection"""
    mocked = mocker.Mock()
    imshow_mock = mocker.Mock()
    mocked.read.return_value = True, np.zeros((100, 100, 3), dtype=np.uint8)
    monkeypatch.setattr(cv2, "VideoCapture", lambda x: mocked)
    monkeypatch.setattr(cv2, "imshow", imshow_mock)
    monkeypatch.setattr(cv2, "waitKey", lambda x: ord("q"))

    model = YOLOv8Pose()
    model.load_model()
    model.detect_webcam()
    args, _ = imshow_mock.call_args
    assert args[1].shape == (100, 100, 3)
    assert args[0].lower() == "YOLOv8".lower()

    monkeypatch.setattr(mocked, "isOpened", lambda: False)
    model.detect_webcam()
    assert imshow_mock.call_count == 1
