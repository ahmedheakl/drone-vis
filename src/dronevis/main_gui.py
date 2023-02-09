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
from dronevis.utils.utils import library_ontro, gui_parse
from termcolor import colored
from dronevis.drone_connect import DemoDrone, Drone
from dronevis.gui.drone_gui import DroneVisGui
import sys
from dronevis.utils import get_logger

def main() -> None:
    """Running CLI script and CLI main loop
    """
   
    args = gui_parse()
    logger = get_logger(debug=args.debug)
    
    if args.drone == "demo":
        drone = DemoDrone(logger=logger)   
    else:
        drone = Drone(logger=logger)
    
    gui = DroneVisGui(drone=drone)
    library_ontro()       
    try:
        gui()
        
    except KeyboardInterrupt:
        print("")
        logger.warning("closing GUI ...")
        gui.on_close_window()
        sys.exit()
        
    except ConnectionError:
        logger.error("Couldn't connect to the drone. Make sure you are connected to the drone network")
        gui.on_close_window()
        
    except AssertionError as error:
        logger.error(error)
        gui.on_close_window()
        
    except (ValueError, AttributeError) as error:
        logger.error(error)
        gui.on_close_window()
        
        
if __name__ == "__main__":
    main()
         


