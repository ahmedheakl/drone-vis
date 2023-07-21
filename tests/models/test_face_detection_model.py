"""Test face detection model"""
import pytest
import numpy as np
import cv2

from dronevis.models.face_detection import FaceDetectModel


@pytest.fixture
def model():
    """Model fixture"""
    face_model = FaceDetectModel()
    yield face_model
    del face_model


def test_face_detect_model_init():
    """Test model initialization"""
    with pytest.raises(TypeError):
        FaceDetectModel(confidence="0.6")

    with pytest.raises(AssertionError):
        FaceDetectModel(confidence=-1)


def test_transform_image(model):
    """Test image transformation"""
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img_out = model.transform_img(img)
    assert np.array_equal(img, img_out)


def test_face_detect_model_predict(model):
    """Test model prediction"""
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img_out = model.predict(img)
    assert img_out.shape == img.shape


def test_predict(mocker):
    """Test model prediction"""
    mp_drawing_mock = mocker.Mock()
    mp_drawing_mock.draw_detection.return_value = None
    mp_module_mock = mocker.Mock()
    mp_module_mock.solutions.face_detection.FaceDetection.return_value = mp_module_mock
    mp_module_mock.process.return_value = mocker.Mock(detections=[])

    fdm = FaceDetectModel()
    fdm.mp_drawing = mp_drawing_mock
    fdm.face_detection = mp_module_mock

    img = np.zeros((100, 100, 3), dtype=np.uint8)
    assert np.array_equal(fdm.predict(img), img)


def test_detect_webcam(monkeypatch, mocker):
    """Test webcam detection"""
    mocked = mocker.Mock()
    imshow_mock = mocker.Mock()
    mocked.read.return_value = True, np.zeros((100, 100, 3), dtype=np.uint8)
    monkeypatch.setattr(cv2, "VideoCapture", lambda x: mocked)
    monkeypatch.setattr(cv2, "imshow", imshow_mock)
    monkeypatch.setattr(cv2, "waitKey", lambda x: ord("q"))

    model = FaceDetectModel()
    model.load_model()
    model.detect_webcam()
    args, _ = imshow_mock.call_args
    assert args[1].shape == (100, 100, 3)
    assert args[0].lower() == "Face Detection".lower()
