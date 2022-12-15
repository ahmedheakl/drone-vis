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
 - dronevis v0.0.2
"""


from time import sleep
from dronevis.drone_connect.drone import Drone

def print_navdata(navdata):
    "Print the navdata as RAW text" 
    print(navdata['navdata_demo']["battery_percentage"])

def main() -> None:
    print("Welcome to dronevis")
    drone = Drone()
    drone.connect()
    # drone.
    # print(drone.list_config())
    drone.set_config(activate_gps=True,activate_navdata=True)
    drone.set_config(max_altitude=50)
    # drone.connect_video()
    print("Getting Navdata ...")
    drone.set_callback(print_navdata)
    sleep(1)
    # drone.takeoff()
    # sleep(10)
    # #drone.forward()
    # drone.land()
    #sleep(2)
    # #drone.takeoff()
    # #sleep(2)
    # #drone.land()
    drone.stop()
    
    
if __name__ == "__main__":
    main()