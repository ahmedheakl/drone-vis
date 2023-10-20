"""DRONE CLI

Connect to your drone and run your CV models

Usage
------------------
    $ dronevis [--options]

Get data about the arguments
    $ dronevis --help

Or just run the following to the default
    $ dronevis

Version
------------------
 - dronevis v1.3.0
"""
from typing import Optional, Sequence
import logging

from dronevis.drone_connect import DemoDrone, Drone
from dronevis.ui.drone_cli import DroneCli
from dronevis.utils.general import library_ontro, init_logger
from dronevis.abstract.base_drone import BaseDrone

_LOG = logging.getLogger(__name__)


def main(arguments: Optional[Sequence[str]] = None) -> None:
    """Running CLI script and CLI main loop"""

    # parse user arguments
    cli = DroneCli()
    args = cli.parse(arguments)
    init_logger(level=args.logger_level)

    # initialize drone instance
    if args.drone == "demo":
        drone: BaseDrone = DemoDrone()
    else:
        drone = Drone()

    # print library ontro
    library_ontro()

    # MAIN LOOP
    try:
        cli(args, drone)

    except KeyboardInterrupt:
        print("")
        _LOG.warning("Keyinterrupt: closing CLI ...")
        drone.stop()

    except NotImplementedError:
        _LOG.error("Drone tests are NOT yet implemented")

    except ConnectionError:
        _LOG.error(
            "Couldn't connect to the drone\n%s",
            "Make sure you are connected to the drone network",
        )

    except (ValueError, AssertionError) as error:
        _LOG.error("An error occured: %s", error)
