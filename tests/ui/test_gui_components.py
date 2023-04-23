"""Test the GUI components module"""
from tkinter import Canvas, Tk

import pytest

from dronevis.ui.gui_components import CircularProgressbar, MainButton, DataFrame
from dronevis.config.gui import MAIN_COLOR, WHITE_COLOR


@pytest.fixture
def canvas():
    """Fixture for creating a canvas"""
    yield Canvas()


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


def test_circular_progressbar_label(canvas):
    """Test the label coordinates of the CircularProgressbar class"""
    bottom_coord = (0, 0)
    top_coord = (100, 100)
    progressbar = CircularProgressbar(canvas, bottom_coord, top_coord)
    label_text = canvas.itemcget(progressbar.label_id, "text")
    assert label_text == "0%"


def test_circular_progressbar_extent(canvas):
    """Test the extent of the CircularProgressbar class"""
    bottom_coord = (0, 0)
    top_coord = (100, 100)
    progressbar = CircularProgressbar(canvas, bottom_coord, top_coord)
    progressbar.extent = 90
    canvas.update()
    arc_extent = canvas.itemcget(progressbar.arc_id, "extent")
    assert arc_extent == "0.0"


def test_circular_progressbar_change(canvas):
    """Test the change of the CircularProgressbar class"""
    bottom_coord = (0, 0)
    top_coord = (100, 100)
    progressbar = CircularProgressbar(canvas, bottom_coord, top_coord)
    progressbar.change(90.0, "data")
    canvas.update()
    arc_extent = canvas.itemcget(progressbar.arc_id, "extent")
    arc_text = canvas.itemcget(progressbar.label_id, "text")
    assert arc_extent == "90.0"
    assert arc_text == "data"


@pytest.fixture
def main_btn():
    """Fixture for creating a main button"""
    root = Tk()
    main_button = MainButton(root, message="Hello, world!")
    yield main_button
    main_button.destroy()
    root.destroy()


def test_main_button_properties(main_btn):
    """Testing main button properties"""
    assert main_btn["background"] == MAIN_COLOR
    assert main_btn["foreground"] == WHITE_COLOR
    assert main_btn["activebackground"] == WHITE_COLOR
    assert main_btn["borderwidth"] == 0
    assert main_btn.message == "Hello, world!"


def test_dataframe_init():
    """Test the initialization of the DataFrame class"""
    root = Tk()
    dataframe = DataFrame(root, title="dronevis")
    assert isinstance(dataframe, DataFrame)
