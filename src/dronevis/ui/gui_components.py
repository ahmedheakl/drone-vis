"""Implementation of a tkinter circular progress bar for the GUI"""
import os
import inspect
from typing import Tuple, Callable
from tkinter import Canvas, Button, messagebox
from tkinter.ttk import Label, Frame
from PIL import Image, ImageTk, ImageOps

import dronevis
from dronevis.config.gui import (
    GREEN_COLOR,
    WHITE_COLOR,
    MAIN_COLOR,
    MAIN_FONT,
    BUTTON_COLOR,
    FONT_COLOR,
    TOGGLE_SIZE,
)


class CircularProgressbar:
    """Circular progress bar implementation for presenting drone navigation data"""

    start_ang: float = 0.0

    def __init__(
        self,
        canvas: Canvas,
        bottom_coord: Tuple[int, int],
        top_coord: Tuple[int, int],
        width: int = 2,
    ) -> None:
        """Contruct circular progressbar
        Args:
            canvas (tkinter.Canvas): a tkinter canvas to render the progressbar
            x0 (int): x pos for bottom oval
            y0 (int): y pos for bottom oval
            x1 (int): x pos for top oval
            y1 (int): y pos for top oval
            width (int, optional): width of circular bar. Defaults to 2.
            start_ang (float, optional): starting angle. Defaults to 0.0.
        """
        self.canvas = canvas

        x0_coords, y0_coords, x1_coords, y1_coords = (
            bottom_coord[0] + width,
            bottom_coord[1] + width,
            top_coord[0] - width,
            top_coord[1] - width,
        )
        self.text_x = (top_coord[0] - bottom_coord[0]) / 2 + 10
        self.text_y = (top_coord[1] - bottom_coord[1]) / 2 + width * 3
        self.width = width
        # draw static bar outline
        mid_width = width / 2
        self.canvas.create_oval(
            x0_coords - mid_width,
            y0_coords - mid_width,
            x1_coords + mid_width,
            y1_coords + mid_width,
            outline=GREEN_COLOR,
        )
        self.canvas.create_oval(
            x0_coords + mid_width,
            y0_coords + mid_width,
            x1_coords - mid_width,
            y1_coords - mid_width,
            outline=GREEN_COLOR,
        )
        self.extent = 0
        self.arc_id = self.canvas.create_arc(
            x0_coords,
            y0_coords,
            x1_coords,
            y1_coords,
            start=self.start_ang,
            extent=0,
            width=self.width,
            style="arc",
            outline="green",
        )
        percent = "0%"
        self.label_id = self.canvas.create_text(
            self.text_x, self.text_y, text=percent, fill="white"
        )

    def change(self, extent: float, text: str) -> None:
        """Change data in the progress bar
        Args:
            extent (float): angle of the progressbar
            text (str): text to be displayed in the middle
        """
        self.canvas.itemconfigure(self.arc_id, extent=extent)
        self.canvas.itemconfigure(self.label_id, text=text)

    def change_canvas(self, canvas: Canvas) -> None:
        """Changed canvas object"""
        self.canvas = canvas


class ImageBWButton(Button):
    """Image button with alternating black/white image"""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        master,
        title: str,
        message: str,
        img: str,
        size: Tuple[int, ...],
        *args,
        **kw,
    ) -> None:
        """Initialize image button
        The button deals with two images ``passive`` and ``active``.
        Each image is used in case of hover/no-hover.

        The active image is an __inverted__ version of the passive.

        Image path is defaulted to be in the assets folder.

        Args:
            master (tkiner.widget): master widget
            title (str): title of info box
            message (str): message to be displayed in info box
            img (str): image path
            size (Tuple[int, ...]): size for image to be resized
            is_inverted (bool): whether to invert the colors
        """
        super().__init__(master, *args, **kw)
        self["background"] = BUTTON_COLOR
        self["activebackground"] = WHITE_COLOR
        package_path = os.path.dirname(inspect.getfile(dronevis))
        passive_img_path = f"{package_path}/assets/{img}"
        passive_img = Image.open(passive_img_path)
        passive_img = passive_img.resize(size, Image.Resampling.HAMMING)
        active_img = ImageOps.invert(passive_img.convert("1"))
        self.passive_img = ImageTk.PhotoImage(passive_img)
        self.active_img = ImageTk.PhotoImage(active_img)
        self["image"] = self.passive_img

        self.message = message
        self.title = title

        self.bind("<Button-3>", self.on_info)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_info(self, _) -> None:
        """Show information about the button

        Args:
            e (tkinter.Event): event information
        """
        messagebox.showinfo(title=self.title, message=self.message)

    def on_enter(self, _) -> None:
        """Event handler for entering hover

        Args:
            e (tkinter.Event): event information
        """
        self["image"] = self.active_img

    def on_leave(self, _) -> None:
        """Event handler for leaving hover

        Args:
            e (tkinter.Event): Event handler for hover
        """
        self["image"] = self.passive_img


class MainButton(Button):
    """Main tkinter button for GUI"""

    def __init__(self, master, message: str, *args, **kw) -> None:
        """Contruct main button style

        Args:
            master (tkiner.Widget): parent of the button
            message (str): message to be displayed in message box
        """
        super().__init__(master, *args, **kw)
        self["foreground"] = FONT_COLOR
        self["background"] = BUTTON_COLOR
        self["activebackground"] = WHITE_COLOR
        self["font"] = MAIN_FONT
        self["borderwidth"] = 0

        self.message = message
        self.bind("<Button-3>", self.on_info)

    def on_info(self, _) -> None:
        """Contruct message box"""
        messagebox.showinfo(title=self["text"], message=self.message)


class DataFrame(Frame):
    """Implementation of Frame for view navigation data"""

    def __init__(self, master: Frame, title: str, *args, **kw) -> None:
        """Contruct a data frame designed for ploting navdata in progressbar style

        Args:
            master (tkinter.ttk.Frame): master frame
            title (str): title to be displayed on top of progressbar
        """
        super().__init__(master, *args, **kw)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.columnconfigure(0, weight=1)

        self.title = title
        self.lbl_title = Label(self, text=self.title)
        self.canvas = Canvas(
            self,
            width=70,
            height=65,
            bd=2,
            bg=MAIN_COLOR,
            highlightthickness=1,
            highlightbackground=MAIN_COLOR,
        )
        self.cpb = CircularProgressbar(
            self.canvas,
            bottom_coord=(10, 0),
            top_coord=(60, 50),
            width=10,
        )

        self.lbl_title.grid(row=0, column=0)
        self.canvas.grid(row=1, column=0)


class ToggleButton(Button):
    """Main tkinter button for GUI"""

    def __init__(
        self, master, open_callback: Callable, close_callback: Callable, *args, **kw
    ) -> None:
        """Contruct main button style

        Args:
            master (tkiner.Widget): parent of the button
            message (str): message to be displayed in message box
        """
        super().__init__(master, *args, **kw)
        package_path = os.path.dirname(inspect.getfile(dronevis))
        on_img_path = f"{package_path}/assets/on.png"
        off_img_path = f"{package_path}/assets/off.png"
        on_img = Image.open(on_img_path)
        on_img = on_img.resize(TOGGLE_SIZE, Image.Resampling.HAMMING)
        off_img = Image.open(off_img_path)
        off_img = off_img.resize(TOGGLE_SIZE, Image.Resampling.HAMMING)
        self.on_img = ImageTk.PhotoImage(on_img)
        self.off_img = ImageTk.PhotoImage(off_img)
        self["image"] = self.off_img
        self["font"] = MAIN_FONT
        self["borderwidth"] = 0
        self.is_on = False
        self.open_callback = open_callback
        self.close_callback = close_callback

        self.bind("<Button-1>", self.on_toggle)

    def on_toggle(self, _) -> None:
        """Contruct message box"""
        if self.is_on:
            self["image"] = self.off_img
            self.close_callback()
        else:
            self["image"] = self.on_img
            self.open_callback()
        self.is_on = not self.is_on

    def change_image(self, image: ImageTk.PhotoImage) -> None:
        """Change image of the button

        Args:
            image (ImageTk.PhotoImage): new image
        """
        self["image"] = image
