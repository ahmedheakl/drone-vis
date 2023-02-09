import logging
import os
import coloredlogs
import sys


def get_logger(debug: bool = False) -> logging.Logger:
    """Initialize logger with desired configs

    Args:
        debug (bool, optional): whether to output debug info to the console. Defaults to False.

    Returns:
        logging.Logger: logger instance with desired configs
    """
    level = logging.DEBUG if debug else logging.INFO
    logs_dir = os.path.join(os.path.expanduser("~"), ".logs")
    logger = logging.getLogger("mainlogger")

    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)

    filename = "dronevis.log"
    logs_path = os.path.join(logs_dir, filename)

    # initialize file handler
    f_handler = logging.FileHandler(filename=logs_path, mode="w")
    c_handler = logging.StreamHandler(sys.stdout)
    
    c_handler.setLevel(level)
    c_format = logging.Formatter("%(asctime)s - %(message)s")
    c_handler.setFormatter(c_format)

    # set configs for file handler
    f_handler.setLevel(logging.DEBUG)
    f_format = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    f_handler.setFormatter(f_format)

    # set handlers
    logger.addHandler(f_handler)
    logger.addHandler(c_handler)

    # initialize colored logs
    
    coloredlogs.install(
        fmt="%(asctime)s - %(message)s",
        logger=logger,
    )

    return logger
