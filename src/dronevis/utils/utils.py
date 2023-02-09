import cv2
import numpy as np
from typing import Union
from pyfiglet import Figlet
from rich import print as rprint
from termcolor import colored
import argparse
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
    if not isinstance(fps, int):
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
    """Parse arguments for the GUI script

    Returns:
        argparse.Namespace: parsed arguments of user input
    """
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
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="whether to output debug info",
    )
       
    args = parser.parse_args()
    return args

def axis_config(ax) -> None:
    """Set the axis paramets for height graph in the GUI

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


    