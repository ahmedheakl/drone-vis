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
 - dronevis-gui v0.2.1
"""
import logging
import sys

from dronevis.utils.utils import library_ontro, gui_parse
from dronevis.drone_connect import DemoDrone, Drone
from dronevis.abstract.base_drone import BaseDrone
from dronevis.gui.drone_gui import DroneVisGui
from dronevis.utils.logger import init_logger


# get logger
init_logger(debug=True)
_LOG = logging.getLogger(__name__)


def main() -> None:
    """Running CLI script and CLI main loop"""

    args = gui_parse()

    if args.drone == "demo":
        drone: BaseDrone = DemoDrone()
    else:
        drone = Drone()

    gui = DroneVisGui(drone=drone)
    library_ontro()
    try:
        gui()

    except KeyboardInterrupt:
        print("")
        _LOG.warning("Closing GUI ...")
        gui.on_close_window()
        sys.exit()

    except (ConnectionError, AssertionError, ValueError, AttributeError) as error:
        _LOG.error(error)
        gui.on_close_window()


if __name__ == "__main__":
    main()
