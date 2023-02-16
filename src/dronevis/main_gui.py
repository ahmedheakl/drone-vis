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

def main() -> None:
    """Running CLI script and CLI main loop
    """
   
    args = gui_parse()
    
    if args.drone == "demo":
        drone = DemoDrone()   
    else:
        drone = Drone()
    
    gui = DroneVisGui(drone=drone)
    library_ontro()       
    try:
        gui()
        
    except KeyboardInterrupt:
        print("\nClosing GUI ...")
        gui.on_close_window()
        sys.exit()
        
    except ConnectionError:
        print(colored("Couldn't connect to the drone. Make sure you are connected to the drone network", "yellow"))
        
    except AssertionError:
        print(colored("Some error occured", "yellow"))
        
    except (ValueError, AttributeError):
        print(colored("Some error occurred, please try again", "yellow"))
        
        
if __name__ == "__main__":
    main()
         


