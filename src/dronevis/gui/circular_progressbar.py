"""Implementation of a tkinter circular progress bar for the GUI"""
from typing import Tuple
from tkinter import Canvas

from dronevis.gui.configs import GREEN_COLOR


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
