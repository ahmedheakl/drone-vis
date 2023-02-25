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
 - dronevis v0.2.2
"""
import sys
import logging

from dronevis.drone_connect import DemoDrone, Drone
from dronevis.ui.drone_cli import DroneCli
from dronevis.utils.general import library_ontro, init_logger
from dronevis.abstract.base_drone import BaseDrone

_LOG = logging.getLogger(__name__)


def main() -> None:
    """Running CLI script and CLI main loop"""

    # parse user arguments
    cli = DroneCli()
    args = cli.parse()
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
        sys.exit()

    except NotImplementedError:
        _LOG.error("Drone tests are NOT yet implemented")

    except ConnectionError:
        _LOG.error("Couldn't connect to the drone")
        _LOG.error("Make sure you are connected to the drone network")

    except (ValueError, AssertionError) as error:
        _LOG.error(error)


if __name__ == "__main__":
    main()
