from tkinter import Canvas
from tkinter.ttk import Label, Frame
from dronevis.gui.configs import MAIN_COLOR
from dronevis.gui.circular_progressbar import CircularProgressbar


class DataFrame(Frame):
    def __init__(self, master: Frame, title: str, *args, **kw) -> None:
        """Contruct a data frame designed for ploting navdata in progressbar style

        Args:
            master (tkinter.ttk.Frame): master frame
            title (str): title to be displayed on top of progressbar
        """
        super(DataFrame, self).__init__(master, *args, **kw)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.columnconfigure(0, weight=1)

        self.title = title
        self.lbl_title = Label(self, text=self.title)
        self.canvas = Canvas(self, width=70, height=65, bd = 2, bg = MAIN_COLOR, highlightthickness  = 1, 
                            highlightbackground = MAIN_COLOR)
        self.cpb = CircularProgressbar(self.canvas, 10, 0, 60, 50, 10)

        self.lbl_title.grid(row=0, column=0)
        self.canvas.grid(row=1, column=0)
