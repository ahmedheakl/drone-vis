"""Test general utitlity functions"""
import os

import torch
import pytest
import cv2
import numpy as np
import matplotlib.pyplot as plt

from dronevis.utils.general import (
    write_fps,
    library_ontro,
    gui_parse,
    axis_config,
    find,
    device,
    download_file,
)
import dronevis.config.gui as cfg

TEST_DATA_PATH = os.getenv("TEST_DATA_PATH", "")
TEST_FPS_IMAGE = TEST_DATA_PATH + "/30fps_image.png"


@pytest.fixture
def fps_image():
    """Fixture for loading test image"""
    image = cv2.imread(TEST_FPS_IMAGE)
    yield image


@pytest.fixture
def axis():
    _, axis = plt.subplots()
    yield axis


def test_write_fps_with_integer(fps_image):
    """Test write_fps with integer input"""
    image = np.zeros((256, 256, 3), dtype=np.uint8)
    fps: int = 30
    image = write_fps(image, fps)
    assert isinstance(image, np.ndarray)
    assert image.shape == (256, 256, 3)
    assert np.array_equal(fps_image, image)


def test_write_fps_with_float(fps_image):
    """Test write_fps with float input"""
    image = np.zeros((256, 256, 3), dtype=np.uint8)
    fps: float = 30.0
    image = write_fps(image, fps)
    assert isinstance(image, np.ndarray)
    assert image.shape == (256, 256, 3)
    assert np.array_equal(fps_image, image)


def test_write_fps_with_int_string(fps_image):
    """Test write_fps with string input"""
    image = np.zeros((256, 256, 3), dtype=np.uint8)
    fps: int = "30"
    image = write_fps(image, fps)
    assert isinstance(image, np.ndarray)
    assert image.shape == (256, 256, 3)
    assert np.array_equal(fps_image, image)


def test_write_fps_with_float_string(fps_image):
    """Test write_fps with string input"""
    image = np.zeros((256, 256, 3), dtype=np.uint8)
    fps: int = "30.0"
    image = write_fps(image, fps)
    assert isinstance(image, np.ndarray)
    assert image.shape == (256, 256, 3)
    assert np.array_equal(fps_image, image)


def test_write_fps_with_invalid_input():
    """Test write_fps with invalid input"""
    image = np.zeros((500, 500, 3), dtype=np.uint8)
    fps = "invalid"
    with pytest.raises(ValueError):
        out_image = write_fps(image, fps)

    fps = ["dronevis"]
    with pytest.raises(AssertionError):
        out_image = write_fps(image, fps)


def test_library_intro(capsys):
    """Test library_ontro function"""
    library_ontro()
    output = capsys.readouterr().out
    assert "Welcome to DroneVis CLI" in output
    assert "DroneVis is a full-compatible library for controlling your drone" in output


def test_gui_parse_real_drone():
    """Test that gui_parse returns real drone args"""
    args = gui_parse(["-d", "real"])
    assert args.drone == "real"


def test_gui_parse_demo_drone():
    """Test that gui_parse returns demo drone args"""
    args = gui_parse(["-d", "demo"])
    assert args.drone == "demo"


def test_gui_parse_default_args():
    """Test that gui_parse returns default args"""
    args = gui_parse([])
    assert args.drone == "demo"
    assert args.logger_level == "info"


def test_gui_parse_invalid_drone_choice():
    """Test that gui_parse raises an error for an invalid drone choice"""
    with pytest.raises(SystemExit):
        gui_parse(["-d", "invalid"])


def test_gui_parse_help_message(capsys):
    """Test that gui_parse displays help message"""
    with pytest.raises(SystemExit):
        gui_parse(["-h"])
    captured = capsys.readouterr()
    assert "DroneVisGUI" in captured.out


def test_axis_config_labels(axis):
    """Test that axis_config sets the correct axis labels"""
    axis_config(axis)
    assert axis.get_xlabel() == "Time"
    assert axis.get_ylabel() == "Height"


def test_axis_config_colors(axis):
    """Test that axis_config sets the correct axis colors"""
    axis_config(axis)
    assert axis.yaxis.label.get_color() == cfg.WHITE_COLOR
    assert axis.xaxis.label.get_color() == cfg.WHITE_COLOR
    assert axis.title.get_color() == cfg.WHITE_COLOR


def test_axis_config_limits(axis):
    """Test that axis_config sets the correct axis limits"""
    axis_config(axis)
    assert axis.get_ylim() == (0.0, float(cfg.GUI_Y_LIMIT))
    assert axis.get_xlim() == (0.0, float(cfg.GUI_X_LIMIT))


def test_find_file_exists_in_current_directory():
    """Test that find returns the correct path for a file that exists in the current directory"""
    file_name = "test_file.txt"
    with open(file_name, "w") as f:
        f.write("test")
    assert find(file_name) == os.path.abspath(file_name)
    os.remove(file_name)


def test_find_file_does_not_exist():
    """Test that find returns an empty string when a file does not exist"""
    assert find("nonexistent_file.txt") == ""


def test_find_file_is_root_directory():
    """Test that find returns an empty string when the file is in the root directory"""
    file_name = "test_file.txt"
    with open(file_name, "w") as f:
        f.write("test")
    assert find(file_name) == os.path.abspath(file_name)
    os.remove(file_name)
    assert find(file_name) == ""


def test_device_returns_cpu_when_cuda_not_available():
    """Test that device returns 'cpu' when cuda is not available"""
    with torch.cuda.device(-1):
        assert device() == "cpu"


def test_device_returns_custom_device_from_environment_variable():
    """Test that device returns a custom device from an environment variable"""
    os.environ["DEVICE"] = "custom_device"
    assert device() == "custom_device"
    del os.environ["DEVICE"]


def test_download_file_returns_cached_file_path():
    """Test that download_file returns the path to a cached file if it exists"""
    file_url = "https://drive.google.com/uc?export=download&id=1FTJWeavbHwmu9Vkr_M5k5mV4Lt8sWGFo"
    file_name = "test_file.pth"
    cache_dir = ".cache/dronevis"
    os.makedirs(cache_dir, exist_ok=True)
    cached_file_path = os.path.join(cache_dir, file_name)
    with open(cached_file_path, "w", encoding="utf-8") as file:
        file.write("test")
    assert cached_file_path in download_file(file_url, file_name)
    os.remove(cached_file_path)
    os.rmdir(cache_dir)
