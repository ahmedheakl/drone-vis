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
    
    
if __name__ == "__main__":
    main()