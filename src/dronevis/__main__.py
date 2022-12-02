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


from dronevis.object_detection_models import SSD

def main() -> None:
    print("Welcome to dronevis")
    ssd = SSD()
    # drone = Drone()
    # drone.connect()
    # print(drone.list_config())
    # drone.set_config(max_altitude=50)
    # drone.connect_video()
    # #drone.emergency()
    # drone.takeoff()
    # sleep(10)
    # #drone.forward()
    # drone.land()
    # #sleep(2)
    # #drone.takeoff()
    # #sleep(2)
    # #drone.land()
    # drone.stop()
    
    
if __name__ == "__main__":
    main()