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
from time import sleep

#from dronevis.object_detection_models import SSD

def print_navdata(navdata):
    "Print the navdata as RAW text" 
    print(navdata['drone_state'])
    print("---------------------------")
    print("---------------------------")
    print(navdata['gps_info'])
    print("---------------------------")
    print("---------------------------")

def main() -> None:
    print("Welcome to dronevis")
    #ssd = SSD()
    drone = Drone()
    drone.connect()
    print(drone.list_config())
    drone.set_config(activate_gps=True,activate_navdata=True)
    drone.set_config(max_altitude=50)

    
    drone.connect_video()
    

    drone.set_callback(print_navdata)
    # #drone.emergency()
    #drone.takeoff()
    sleep(5)
    # #drone.forward()
    # drone.land()
    #sleep(20)
    # #drone.takeoff()
    # #sleep(2)
    #drone.land()

    #sleep(1)
    print("stop-------------------------------------------")
    drone.stop()
    
    
if __name__ == "__main__":
    main()