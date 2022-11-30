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

def get_vid_stream() -> None:
    """Retrieve video stream from drone cam
    """
    cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
    running = True
    while running:
        # get current frame of video
        running, frame = cam.read()
        if running:
            cv2.imshow('frame', frame)
            cv2.imwrite("frame.jpg", frame)
            if cv2.waitKey(1) & 0xFF == 27: 
                # escape key pressed
                running = False
        else:
            # error reading frame
            print('error reading video feed')
    cam.release()
    cv2.destroyAllWindows()

import cv2
def main() -> None:
    """Main script
    """
    print("Welcome to dronevis")
    get_vid_stream()
from dronevis.drone_connect.drone import Drone
from time import sleep
import socket

def main() -> None:
    print("Welcome to dronevis")

    drone = Drone()
    drone.connect()
    print(drone.list_config())
    drone.set_config(max_altitude=50)
    drone.connect_video()
    #drone.emergency()
    drone.takeoff()
    sleep(10)
    #drone.forward()
    drone.land()
    #sleep(2)
    #drone.takeoff()
    #sleep(2)
    #drone.land()
    drone.stop()
    
    
if __name__ == "__main__":
    main()