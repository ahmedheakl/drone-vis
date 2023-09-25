"""Test the GUI components module"""
from tkinter import Canvas, Tk
import os

import pytest

from dronevis.ui.gui_components import CircularProgressbar, MainButton, DataFrame
from dronevis.config.gui import BUTTON_COLOR, WHITE_COLOR, FONT_COLOR


@pytest.fixture
def canvas(mocker):
    """Fixture for creating a canvas"""
    # return mocked canvas
    mocked_canvas = mocker.Mock(spec=Canvas)

    mocked_canvas.coords.return_value = [2, 2, 98, 98]
    mocked_canvas.itemcget.return_value = "0.0"

    return mocked_canvas


def test_circular_progressbar_init(canvas):
    """Test the initialization of the CircularProgressbar class"""
    bottom_coord = (0, 0)
    top_coord = (100, 100)
    width = 5
    progressbar = CircularProgressbar(canvas, bottom_coord, top_coord, width=width)
    assert progressbar.canvas == canvas
    assert progressbar.width == width


def test_circular_progressbar_text_coords(canvas):
    """Test the text coordinates of the CircularProgressbar class"""
    bottom_coord = (0, 0)
    top_coord = (100, 100)
    progressbar = CircularProgressbar(canvas, bottom_coord, top_coord)
    assert progressbar.text_x == 60
    assert progressbar.text_y == 56.0


def test_circular_progressbar_arc(canvas):
    """Test the arc coordinates of the CircularProgressbar class"""
    bottom_coord = (0, 0)
    top_coord = (100, 100)
    progressbar = CircularProgressbar(canvas, bottom_coord, top_coord)
    arc_coords = canvas.coords(progressbar.arc_id)
    assert arc_coords == [2, 2, 98, 98]


# Skip this if not $display variable
@pytest.mark.skipif(os.environ.get("DISPLAY") is None, reason="requires display")
def test_circular_progressbar_label():
    """Test the label coordinates of the CircularProgressbar class"""
    canvas = Canvas()
    bottom_coord = (0, 0)
    top_coord = (100, 100)
    progressbar = CircularProgressbar(canvas, bottom_coord, top_coord)
    label_text = canvas.itemcget(progressbar.label_id, "text")
    assert label_text == "0%"
    canvas.destroy()


def test_circular_progressbar_extent(canvas):
    """Test the extent of the CircularProgressbar class"""
    bottom_coord = (0, 0)
    top_coord = (100, 100)
    progressbar = CircularProgressbar(canvas, bottom_coord, top_coord)
    progressbar.extent = 90
    canvas.update()
    arc_extent = canvas.itemcget(progressbar.arc_id, "extent")
    assert arc_extent == "0.0"


@pytest.fixture
def main_btn():
    """Fixture for creating a main button"""
    root = Tk()
    main_button = MainButton(root, message="Hello, world!")
    yield main_button
    main_button.destroy()


@pytest.mark.skipif(os.environ.get("DISPLAY") is None, reason="requires display")
def test_main_button_properties(main_btn):
    """Testing main button properties"""
    assert main_btn["background"] == BUTTON_COLOR
    assert main_btn["foreground"] == FONT_COLOR
    assert main_btn["activebackground"] == WHITE_COLOR
    assert main_btn["borderwidth"] == 0
    assert main_btn.message == "Hello, world!"


@pytest.mark.skipif(os.environ.get("DISPLAY") is None, reason="requires display")
@pytest.mark.skipif()
def test_dataframe_init(mocker):
    """Test the initialization of the DataFrame class"""
    root = Tk()
    root.winfo_screenwidth.return_value = 1920
    root.tk = mocker.Mock()
    dataframe = DataFrame(root, title="dronevis")
    assert isinstance(dataframe, DataFrame)
