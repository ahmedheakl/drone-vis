"""Utilities for dronevis library including image processing and parser"""
from typing import Union, Optional, Sequence
import logging
import os
import argparse

from pyfiglet import Figlet
from rich import print as rprint
from termcolor import colored
from rich_argparse import RichHelpFormatter
import cv2
import numpy as np
import coloredlogs
import wget
import torch

from dronevis import __version__
import dronevis.config.gui as cfg


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
        fps = str(int(float(fps)))

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


def gui_parse(arguments: Optional[Sequence[str]] = None) -> argparse.Namespace:
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
        "--log-level",
        dest="logger_level",
        type=str,
        choices=["debug", "info", "warning", "error", "critical"],
        default="info",
        help="Level for logger",
    )

    args = parser.parse_args(arguments)
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


def find(file_name: str) -> str:
    """Searches for a file in the directory and all its parents"""
    cur_dir = os.getcwd()
    while True:
        file_list = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if file_name in file_list:
            return os.path.join(cur_dir, file_name)
        if cur_dir == parent_dir:  # if dir is root dir
            return ""

        cur_dir = parent_dir


def init_logger(level: Union[int, str] = logging.INFO) -> None:
    """Initialize logger with desired configs

    Args:
        debug (bool, optional): Whether to output debug info to the console. Defaults to False.

    Returns:
        logging.Logger: Logger instance with desired configs
    """
    to_log_level = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    if isinstance(level, str):
        assert level in to_log_level, "Invalid level name"
        log_level = to_log_level[level]
    else:
        log_level = level

    logs_dir = os.path.join(os.path.expanduser("~"), ".logs")

    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)

    filename = "dronevis.log"
    logs_path = os.path.join(logs_dir, filename)

    # initialize file handler
    f_handler = logging.FileHandler(filename=logs_path, mode="w")
    f_handler.setLevel(logging.DEBUG)
    f_format = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    f_handler.setFormatter(f_format)

    # set handlers
    logging.basicConfig(handlers=[f_handler])

    # initialize colored logs
    coloredlogs.install(
        fmt="%(asctime)s - %(message)s",
        level=log_level,
    )


def download_file(file_url: str, file_name: str) -> str:
    """Download file from url"""

    # Define the path to the .cache directory for each operating system
    if os.name == "nt":  # Windows
        cache_dir = os.path.join(os.environ["LOCALAPPDATA"], ".cache/dronevis")
    elif os.name == "posix":  # Linux or Mac
        cache_dir = os.path.join(os.environ["HOME"], ".cache/dronevis")
    else:
        raise OSError("Unsupported operating system")

    os.makedirs(cache_dir, exist_ok=True)
    model_weights_path = os.path.join(cache_dir, file_name)

    if os.path.exists(model_weights_path):
        return model_weights_path

    wget.download(file_url, model_weights_path)

    return model_weights_path


def device() -> torch.device:
    """Returns the device to be used for inference"""
    device_name = os.getenv("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
    device_type = torch.device(device_name)
    return device_type
