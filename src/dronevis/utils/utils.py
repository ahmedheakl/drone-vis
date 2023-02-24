"""Utilities for dronevis library including image processing and parser"""
from typing import Union
import argparse
from pyfiglet import Figlet
from rich import print as rprint
from termcolor import colored
from rich_argparse import RichHelpFormatter
import cv2
import numpy as np

import dronevis.gui.configs as cfg
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
        "DroneVis is a full-compatible library for [green]controlling your drone [white]and"
        + "\nrunning your favourite [green]computer vision algorithms in real-time[white]"
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
        "-v", "--version", action="version", version=f"Version: {__version__}"
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


def axis_config(axis) -> None:
    """Set the axis paramets for height graph in the GUI

    Args:
        ax (plt.ax): matplotlib axis
    """
    axis.legend(["height"])
    axis.set_xlabel("Time")
    axis.set_ylabel("Height")
    axis.yaxis.label.set_color(cfg.WHITE_COLOR)
    axis.xaxis.label.set_color(cfg.WHITE_COLOR)
    axis.title.set_color(cfg.WHITE_COLOR)
    axis.spines["bottom"].set_color(cfg.WHITE_COLOR)
    axis.spines["top"].set_color(cfg.WHITE_COLOR)
    axis.spines["right"].set_color(cfg.WHITE_COLOR)
    axis.spines["left"].set_color(cfg.WHITE_COLOR)
    axis.tick_params(axis="x", colors=cfg.WHITE_COLOR)
    axis.tick_params(axis="y", colors=cfg.WHITE_COLOR)
    axis.set_facecolor(cfg.MAIN_COLOR)
    axis.set_ylim([0, cfg.GUI_Y_LIMIT])
    axis.set_xlim([0, cfg.GUI_X_LIMIT])
