from tkinter import Button, Event, messagebox
from typing import Tuple
from dronevis.gui.configs import * 
from PIL import Image, ImageTk
import inspect
import os 
import dronevis


class ImageButton(Button):
    def __init__(
        self,
        master,
        title: str,
        message: str,
        passive_img_path: str,
        active_img_path: str,
        size: Tuple[int, ...],
        *args,
        **kw
    ) -> None:
        super(ImageButton, self).__init__(master, *args, **kw)
        
        self.title = title
        self.message = message
        
        self["background"] = MAIN_COLOR
        self["activebackground"] = WHITE_COLOR
        
        # get path of library is site-packages
        package_path = os.path.dirname(inspect.getfile(dronevis))
        
        # get path of images
        passive_img_path = f"{package_path}/assets/{passive_img_path}"
        active_img_path = f"{package_path}/assets/{active_img_path}"
        
        # load images
        passive_img = Image.open(passive_img_path)
        active_img = Image.open(active_img_path)
        
        # resize images
        passive_img = passive_img.resize(size, Image.Resampling.HAMMING)
        active_img = active_img.resize(size, Image.Resampling.HAMMING)
        
        
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
