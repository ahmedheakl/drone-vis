"""Testing pose estimation module"""
import pytest
import numpy as np

from dronevis.models.pose_mediapipe import PoseSegEstimation, cv2


@pytest.fixture
def pose_model():
    """Fixture for loading pose estimation model"""
    model = PoseSegEstimation()
    model.load_model()
    yield model
    del model


def test_multiple_return_type() -> None:
    """Testing whether the model does not allow multiple but
    conflicting inferences"""
    with pytest.raises(AssertionError) as _:
        PoseSegEstimation(is_seg=True, is_seg_pose=True)


def test_transform_image(pose_model: PoseSegEstimation):
    """Test image transformation"""
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    transformed = pose_model.transform_img(image)
    assert transformed.shape == image.shape
    assert transformed.dtype == image.dtype


def test_model_is_not_none(pose_model):
    """Test whether the model is loaded"""
    assert pose_model.net is not None


def test_model_prediction(pose_model):
    """Test model prediction"""
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    output1 = pose_model.predict(image, is_seg=True)[0]
    assert isinstance(output1, np.ndarray)
    assert output1.shape == image.shape
    assert output1.dtype == np.uint8


def test_detect_webcam_assert_error():
    """Test whether the model raises an error when
    the model is not loaded
    """
    model = PoseSegEstimation()
    with pytest.raises(AssertionError):
        model.detect_webcam()


def test_detect_webcam(monkeypatch, mocker):
    """Test webcam detection"""
    mocked = mocker.Mock()
    imshow_mock = mocker.Mock()
    mocked.read.return_value = True, np.zeros((100, 100, 3), dtype=np.uint8)
    monkeypatch.setattr(cv2, "VideoCapture", lambda x: mocked)
    monkeypatch.setattr(cv2, "imshow", imshow_mock)
    monkeypatch.setattr(cv2, "waitKey", lambda x: ord("q"))

    # Create a PoseSegEstimation object and call the detect_webcam() method
    model = PoseSegEstimation()
    model.load_model()
    model.detect_webcam()
    args, _ = imshow_mock.call_args
    assert args[1].shape == (100, 100, 3)
    assert args[0].lower() == "Segmented Pose".lower()
