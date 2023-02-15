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
from typing import Union
import sys
import logging

from dronevis.drone_connect import DemoDrone, Drone
from dronevis.cli import DroneCli
from dronevis.utils.utils import library_ontro
from dronevis.utils.logger import init_logger

# get logger
init_logger()
_LOG = logging.getLogger(__name__)


def main() -> None:
    """Running CLI script and CLI main loop"""

    # parse user arguments
    cli = DroneCli()
    args = cli.parse()

    # initialize drone instance
    if args.drone == "demo":
        drone: Union[Drone, DemoDrone] = DemoDrone()
    else:
        drone = Drone()

    # print library ontro
    library_ontro()

    # MAIN LOOP
    try:
        cli(args, drone)

    except KeyboardInterrupt:
        print("")
        _LOG.warning("keyinterrupt: closing CLI ...")
        drone.stop()
        sys.exit()

    except NotImplementedError:
        _LOG.error("drone tests are NOT yet implemented")

    except ConnectionError:
        _LOG.error("couldn't connect to the drone")
        _LOG.error("make sure you are connected to the drone network")

    except (ValueError, AssertionError) as error:
        _LOG.error(error)


if __name__ == "__main__":
    main()
