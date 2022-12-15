from tkinter import Canvas
from dronevis.gui.configs import WHITE_COLOR, GREEN_COLOR


class CircularProgressbar:
    def __init__(
        self,
        canvas: Canvas,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        width: int = 2,
        start_ang: float = 0.0,
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
        self.x0, self.y0, self.x1, self.y1 = (
            x0 + width,
            y0 + width,
            x1 - width,
            y1 - width,
        )
        self.tx, self.ty = (x1 - x0) / 2 + 10, (y1 - y0) / 2 + width * 3
        self.width = width
        self.start_ang = start_ang
        # draw static bar outline
        w2 = width / 2
        self.oval_id1 = self.canvas.create_oval(
            self.x0 - w2, self.y0 - w2, self.x1 + w2, self.y1 + w2, outline=GREEN_COLOR
        )
        self.oval_id2 = self.canvas.create_oval(
            self.x0 + w2, self.y0 + w2, self.x1 - w2, self.y1 - w2, outline=GREEN_COLOR
        )
        self.extent = 0
        self.arc_id = self.canvas.create_arc(
            self.x0,
            self.y0,
            self.x1,
            self.y1,
            start=self.start_ang,
            extent=0,
            width=self.width,
            style="arc",
            outline="green",
        )
        percent = "0%"
        self.label_id = self.canvas.create_text(
            self.tx, self.ty, text=percent, fill="white"
        )

    def change(self, extent: float, text: str) -> None:
        """Change data in the progress bar

        Args:
            extent (float): angle of the progressbar
            text (str): text to be displayed in the middle
        """
        self.canvas.itemconfigure(self.arc_id, extent=extent)
        self.canvas.itemconfigure(self.label_id, text=text)
