from tkinter import Button, messagebox, Event
from dronevis.gui.configs import WHITE_COLOR, MAIN_COLOR, MAIN_FONT


class MainButton(Button):
    def __init__(self, master, message: str, *args, **kw) -> None:
        """Contruct main button style

        Args:
            master (tkiner.Widget): parent of the button
            message (str): message to be displayed in message box
        """
        super(MainButton, self).__init__(master, *args, **kw)
        self["foreground"] = WHITE_COLOR
        self["background"] = MAIN_COLOR
        self["activebackground"] = WHITE_COLOR
        self["font"] = MAIN_FONT
        self["borderwidth"] = 0

        self.message = message
        self.bind("<Button-3>", self.on_info)

    def on_info(self, e: Event) -> None:
        """Contruct message box

        Args:
            e (tkinter.Event): event information
        """
        messagebox.showinfo(title=self["text"], message=self.message)
