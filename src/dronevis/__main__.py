"""Connect to your drone and run your CV models
Usage
------------------
    
    $ dronevis [--options]
Get data about the arguments
    $ dronevis -help
Or just run the following to the default
    
    $ dronevis
    
    
Version
------------------
 - dronevis v0.0.1
"""
from dronevis.drone_connect.drone import Drone

def main() -> None:
    print("Welcome to dronevis")
    drone = Drone()
    
    
if __name__ == "__main__":
    main()