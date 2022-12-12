from tkinter import Button, messagebox, Event
import dronevis
import os
import inspect
from dronevis.gui.configs import WHITE_COLOR, MAIN_COLOR
from PIL import Image, ImageTk, ImageOps
from typing import Tuple


class ImageBWButton(Button):
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
        super(ImageBWButton, self).__init__(master, *args, **kw)
        self["background"] = MAIN_COLOR
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

    def on_info(self, e: Event) -> None:
        """Show information about the button

        Args:
            e (tkinter.Event): event information
        """
        messagebox.showinfo(title=self.title, message=self.message)

    def on_enter(self, e: Event) -> None:
        """Event handler for entering hover

        Args:
            e (tkinter.Event): event information
        """
        self["image"] = self.active_img
        
    def on_leave(self, e: Event) -> None:
        """Event handler for leaving hover

        Args:
            e (tkinter.Event): Event handler for hover
        """
        self["image"] = self.passive_img

