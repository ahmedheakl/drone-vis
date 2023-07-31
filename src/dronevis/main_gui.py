"""DRONE GUI

Connect to your drone and run your CV models

Usage
------------------

    $ dronevis-gui [--options]

Get data about the arguments
    $ dronevis-gui --help

Or just run the following to the default
    $ dronevis-gui

Version
------------------
 - dronevis-gui v1.1.0
"""
from typing import Optional, Sequence
import logging

from dronevis.utils.general import library_ontro, gui_parse, init_logger
from dronevis.drone_connect import DemoDrone, Drone
from dronevis.abstract.base_drone import BaseDrone
from dronevis.ui.drone_gui import DroneVisGui


_LOG = logging.getLogger(__name__)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """Running CLI script and CLI main loop"""

    args = gui_parse(argv)
    init_logger(level=args.logger_level)

    if args.drone == "demo":
        drone: BaseDrone = DemoDrone()
    else:
        drone = Drone()

    gui = DroneVisGui(drone=drone)
    library_ontro()
    try:
        gui()

    except KeyboardInterrupt as exec_info:
        print("")
        _LOG.warning("Closing GUI ...")
        gui.on_close_window()
        raise SystemExit(1) from exec_info

    except (ConnectionError, AssertionError, ValueError, AttributeError) as exec_info:
        _LOG.error(exec_info)
        gui.on_close_window()
        raise SystemExit(1) from exec_info


if __name__ == "__main__":
    main()
