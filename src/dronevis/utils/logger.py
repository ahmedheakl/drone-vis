"""Logger helper functions"""
import logging
import os
import coloredlogs


def init_logger(debug: bool = False) -> None:
    """Initialize logger with desired configs

    Args:
        debug (bool, optional): whether to output debug info to the console. Defaults to False.

    Returns:
        logging.Logger: logger instance with desired configs
    """
    level = logging.DEBUG if debug else logging.INFO
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
        level=level,
    )
