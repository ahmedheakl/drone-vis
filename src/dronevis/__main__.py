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

from termcolor import colored
from dronevis.drone_connect import DemoDrone, Drone
from dronevis.cli import DroneCli
import sys
from dronevis.utils import library_ontro

def main() -> None:
    """Running CLI script and CLI main loop
    """
    
    # parse user arguments
    cli = DroneCli()
    args = cli.parse()
    
    # initialize drone instance
    if args.drone == "demo":
        drone = DemoDrone()   
    else:
        drone = Drone()
    
    # print library ontro
    library_ontro()
       
       
    # MAIN LOOP
    try:
        cli(args, drone)
        
    except KeyboardInterrupt:
        print("\nClosing CLI ...")
        drone.stop()
        sys.exit()
    
    except NotImplementedError:
        print(colored("Drone tests are NOT yet implemented", "yellow"))
        
    except ConnectionError:
        print(colored("Couldn't connect to the drone. Make sure you are connected to the drone network", "yellow"))
        
    except AssertionError:
        print(colored("Please enter a valid drone instance", "yellow"))
        
    except (ValueError, AttributeError):
        print(colored("Some error occurred, please try again", "yellow"))
        
        
if __name__ == "__main__":
    main()
         


