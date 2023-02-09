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

from dronevis.drone_connect import DemoDrone, Drone
from dronevis.cli import DroneCli
import sys
from dronevis.utils import library_ontro
from dronevis.utils import get_logger


def main() -> None:
    """Running CLI script and CLI main loop"""

    # parse user arguments
    cli = DroneCli()
    args = cli.parse()

    logger = get_logger(debug=args.debug)

    # initialize drone instance
    if args.drone == "demo":
        drone = DemoDrone(logger=logger)
    else:
        drone = Drone(logger=logger)

    # print library ontro
    library_ontro()

    # MAIN LOOP
    try:
        cli(args, drone)

    except KeyboardInterrupt:
        print("")
        logger.warning("keyinterrupt: closing CLI ...")
        drone.stop()
        sys.exit()

    except NotImplementedError:
        logger.error("drone tests are NOT yet implemented")

    except ConnectionError:
        logger.error("couldn't connect to the drone")
        logger.error("make sure you are connected to the drone network")
        
    except (ValueError, AssertionError) as error:
        logger.error(error)

if __name__ == "__main__":
    main()
