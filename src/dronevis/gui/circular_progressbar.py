"""Implementation of a tkinter circular progress bar for the GUI"""
from typing import Tuple
from tkinter import Canvas

from dronevis.gui.configs import GREEN_COLOR


class CircularProgressbar:
    """Progress bar for Tkinter GUI"""

    start_ang = 0.0

    def __init__(
        self,
        canvas: Canvas,
        bottom_coord: Tuple[int, int],
        top_coord: Tuple[int, int],
        width: int = 2,
    ) -> None:
        """Construct circular progressbar

        Args:
            canvas (tkinter.Canvas): Tkinter canvas to render the progressbar
            bottom_coord (Tuple[int, int]): Coordinates for bottom oval
            top_coord(Tuple[int, int]): Coordinates for top oval
        """
        self.canvas = canvas
        x0_coord, y0_coord, x1_coord, y1_coord = (
            bottom_coord[0] + width,
            bottom_coord[1] + width,
            top_coord[0] - width,
            top_coord[1] - width,
        )
        label_x = (x1_coord - x0_coord) / 2 + 10
        label_y = (y1_coord - y0_coord) / 2 + width * 3
        # draw static bar outline
        mid_point = width / 2
        self.canvas.create_oval(
            x0_coord - mid_point,
            y0_coord - mid_point,
            x1_coord + mid_point,
            y1_coord + mid_point,
            outline=GREEN_COLOR,
        )
        self.canvas.create_oval(
            x0_coord + mid_point,
            y0_coord + mid_point,
            x1_coord - mid_point,
            y1_coord - mid_point,
            outline=GREEN_COLOR,
        )
        self.arc_id = self.canvas.create_arc(
            x0_coord,
            y0_coord,
            x1_coord,
            y1_coord,
            start=self.start_ang,
            extent=0,
            width=width,
            style="arc",
            outline="green",
        )
        self.label_id = self.canvas.create_text(
            label_x,
            label_y,
            text="0%",
            fill="white",
        )

    def change(self, extent: float, text: str) -> None:
        """Change data in the progress bar

        Args:
            extent (float): Angle of the progressbar
            text (str): Text to be displayed in the middle
        """
        self.canvas.itemconfigure(self.arc_id, extent=extent)
        self.canvas.itemconfigure(self.label_id, text=text)

    def set_start_ang(self, start_ang: float) -> None:
        """Setter of start angle instance variable"""
        self.start_ang = start_ang
