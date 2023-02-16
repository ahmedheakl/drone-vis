import cv2
import numpy as np
from typing import Union
from pyfiglet import Figlet
from rich import print as rprint
from termcolor import colored
import argparse
import os
import os.path
from rich_argparse import RichHelpFormatter
from dronevis.gui.configs import *
from dronevis import __version__

def write_fps(image: np.ndarray, fps: Union[str, int, float]) -> np.ndarray:
    """Write fps on input image

    Args:
        image (np.array): input image
        fps (Union[str, int, float]): frame per second

    Returns:
        np.array: processed image with fps written
    """
    assert isinstance(fps, (str, int, float)), "Please enter a valid fps value"
    if not isinstance(fps, str):
        fps = str(int(fps))

    cv2.putText(
        img=image,
        text=f"{fps} FPS",
        org=(15, 30),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=1,
        color=(100, 200, 0),
        thickness=2,
    )
    return image


def library_ontro() -> None:
    """Print pretty output from dronevis ontro"""
    print(colored(Figlet(font="big").renderText("DRONE VIS"), "green"))
    rprint("[violet]Welcome to DroneVis CLI")
    rprint(
        "DroneVis is a full-compatible library for [green]controlling your drone [white]and\nrunning your favourite [green]computer vision algorithms in real-time[white]"
    )
    print("----------------------------------------------------------")


def gui_parse() -> argparse.Namespace:
    
    parser = argparse.ArgumentParser(
        prog="DroneVisGUI",
        description="Parser arguments to run dronevis GUI",
        epilog="Enjoy the drone experience! \N{slightly smiling face}",
        formatter_class=RichHelpFormatter,
    )
    
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Version: {__version__}"
    )
    
    parser.add_argument(
        "-d",
        "--drone",
        type=str,
        default="demo",
        dest="drone",
        choices=["demo", "real"],
        help="whether to use a demo drone or a real drone",        
    )
       
    args = parser.parse_args()
    return args

def axis_config(ax) -> None:
    """Set the axis paramets for height graph

    Args:
        ax (plt.ax): matplotlib axis
    """
    ax.legend(["height"])
    ax.set_xlabel("Time")
    ax.set_ylabel("Height")
    ax.yaxis.label.set_color(WHITE_COLOR)
    ax.xaxis.label.set_color(WHITE_COLOR)
    ax.title.set_color(WHITE_COLOR)
    ax.spines["bottom"].set_color(WHITE_COLOR)
    ax.spines["top"].set_color(WHITE_COLOR)
    ax.spines["right"].set_color(WHITE_COLOR)
    ax.spines["left"].set_color(WHITE_COLOR)
    ax.tick_params(axis="x", colors=WHITE_COLOR)
    ax.tick_params(axis="y", colors=WHITE_COLOR)
    ax.set_facecolor(MAIN_COLOR)
    ax.set_ylim([0, GUI_Y_LIMIT])
    ax.set_xlim([0, GUI_X_LIMIT])

def find (file_name)-> str:
    """Searches for a file in the directory and all it's parents

    Args:
        file_name: string of the name of the file
    """
    cur_dir = os.getcwd() 
    while True:
        file_list = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if file_name in file_list:
            return os.path.join(cur_dir,file_name)
            break
        else:
            if cur_dir == parent_dir: #if dir is root dir
                return None
            else:
                cur_dir = parent_dir


    