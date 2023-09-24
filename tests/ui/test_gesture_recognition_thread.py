"""Test gesture recognition thread"""
from tkinter.ttk import Label

from dronevis.ui.gesture_recognition_thread import GestureThread


def test_init():
    """Test initailization"""
    label = Label()
    thread = GestureThread(label)
    assert thread.model.hands is None
    assert thread.video_index == 0
    assert thread.label == label
    assert thread.running


def test_run():
    """Test run"""
    label = Label()
    thread = GestureThread(label)
    thread.start()
    thread.join()
    assert not thread.running


def test_resume():
    """Test resume"""
    label = Label()
    thread = GestureThread(label)
    thread.start()
    thread.resume()
    thread.join()
    assert not thread.running


def test_stop():
    """Test stop"""
    label = Label()
    thread = GestureThread(label)
    thread.start()
    thread.stop()
    thread.join()
    assert not thread.running
