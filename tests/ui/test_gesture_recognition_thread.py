"""Test gesture recognition thread"""
import pytest
import cv2
import numpy as np

from dronevis.ui.gesture_recognition_thread import GestureThread


def test_init(mocker):
    """Test initailization"""
    label = mocker.Mock()

    label.configure = lambda x: None
    label.after = lambda *args: None
    thread = GestureThread(label)
    assert thread.model.hands is None
    assert thread.video_index == 0
    assert thread.label == label
    assert thread.running


def test_run(monkeypatch: pytest.MonkeyPatch, mocker):
    """Test run"""
    label = mocker.Mock()

    label.configure = lambda x: None
    label.after = lambda *args: None
    mocked = mocker.Mock()
    imshow_mock = mocker.Mock()
    mocked.read.return_value = True, np.zeros((100, 100, 3), dtype=np.uint8)
    monkeypatch.setattr(cv2, "VideoCapture", lambda x: mocked)
    monkeypatch.setattr(cv2, "imshow", imshow_mock)
    monkeypatch.setattr(cv2, "waitKey", lambda x: ord("q"))
    thread = GestureThread(label)
    thread.start()
    thread.join()
    assert thread.running


def test_stop(monkeypatch: pytest.MonkeyPatch, mocker):
    """Test stop"""
    label = mocker.Mock()

    label.configure = lambda x: None
    label.after = lambda *args: None
    mocked = mocker.Mock()
    imshow_mock = mocker.Mock()
    mocked.read.return_value = True, np.zeros((100, 100, 3), dtype=np.uint8)
    monkeypatch.setattr(cv2, "VideoCapture", lambda x: mocked)
    monkeypatch.setattr(cv2, "imshow", imshow_mock)
    monkeypatch.setattr(cv2, "waitKey", lambda x: ord("q"))
    thread = GestureThread(label)
    thread.start()
    thread.stop()
    thread.join()
    assert not thread.running
