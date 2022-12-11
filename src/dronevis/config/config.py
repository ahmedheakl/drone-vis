def activate_navdata(activate=True):
    "Prepare the drone so he can send navdata back to us"
    if activate:
        return [("general:navdata_demo","FALSE")] #Activate navdata
    else:
        return [("general:navdata_demo","TRUE")]
def activate_gps(activate=True):
    "Prepare the drone to receive GPS command"
    if activate:
        return [("control:flying_mode","0"),("control:autonomous_flight","FALSE")]
    else:
        return []
def detect_tag(color=0):
    """ Send the config to the drone to activate drone detection
        0 is the blue-orange color
        1 is the yellow-orange color"""
    if color == 1:
        tag_color = "2"
    else:           tag_color = "3"
    com = list()
    com.append(("detect:detect_type","13"))
    com.append(("detect:enemy_colors",tag_color))
    com.append(("detect:enemy_without_shell","0"))
    return com

# ONE-TIME CONFIG RELATED
def indoor(activate = True):
    "Set the drone config to act as if it is indoor"
    if activate:
        return [("control:outdoor","FALSE"),("control:flight_without_shell","FALSE")]
    else:
        return outdoor(activate=True)
def outdoor(activate = True):
    "Set the drone config to act as if it is outdoor"
    if activate:
        return [("control:outdoor","TRUE"),("control:flight_without_shell","TRUE")]
    else:
        return indoor(activate=True)

def nervosity_level(percentage=20):
    "Configure the nervosity of the drone,percentage=10:weak response to command; percentage=100:full trust"
    euler = int(0.52*percentage)/100.0 # 2 digits after coma
    vertical_speed = int(2000*percentage)
    yaw = int(6.11*percentage)/100.0
    com = list()
    com.append(("control:euler_angle_max",str(euler)))
    com.append(("control:control_vz_max",str(vertical_speed)))
    com.append(("control:control_yaw",str(yaw)))
    return com
def max_altitude(altitude=5):
    "Set the max altitude of the drone"
    return [("control:altitude_max",str(int(altitude*1000)))]

'''
def set_ultrasound(freq=0):
    "Set the ultrasound frequence"
    if freq:    return [("pic:ultrasound_freq","7")]
    else:       return [("pic:ultrasound_freq","8")]
'''
def activate_video(activate = True):
    "Start/Stop the recording of a video on the USB key"
    if activate:
        return [("video:video_codec","128")]
    else:
        return []         
    
# Animations
def flip(side="LEFT"):
    """ Do a flip, side is the side of the flip
        Side is LEFT, RIGHT, FRONT, BACK"""
    s = 17
    if side.upper() == "FRONT": s = 16
    if side.upper() == "LEFT":  s = 18
    if side.upper() == "RIGHT": s = 19
    return [("control:flight_anim",str(s)+",15")]

# Autonomous Flight
def goto_gps_point(latitude, longitude, altitude=2, cap=0, speed=1, continuous=False):
    "Send the drone to the GPS point, cap is in degre"
    if (longitude == 0) or (latitude == 0):   return [] # Try not to send drone to somewhere weird
    # Compute each data
    longi = int(longitude*10000000)
    lati = int(latitude*10000000)
    alt = int(altitude*1000)
    cap = int(cap)
    # Create the right parameter according to doc
    param1 = "10000,1500,"+str(lati)+","+str(longi)+","+str(alt)+",0,0,0," + str(cap) + ",0"
    # Let's go !
    com = list()
    #if not continuous:  com.append(("control:flying_mode","0")) # To Check
    #if not continuous:  com.append(("control:autonomous_flight","FALSE")) # To Check
    if not continuous:  com.append(("control:flying_camera_enable","FALSE"))
    com.append(("control:flying_camera_mode",param1))
    if not continuous:  com.append(("control:flying_camera_enable","TRUE"))
    return com

###############
### GLOBALS ###
###############

SUPPORTED_CONFIG = {
    "detect_tag":detect_tag, "activate_navdata":activate_navdata, "activate_gps":activate_gps,           # Data activation
    "indoor":indoor, "outdoor":outdoor, "nervosity_level":nervosity_level, "max_altitude":max_altitude,# One-time config
    
    }
AUTONOMOUS_FLIGHT = {"gps":goto_gps_point}
ANIMATIONS = {"flip":flip}
ANIMATIONS_INFOS = {"flip":"(side)"}
# Check if animations corelate
if ANIMATIONS.keys() != ANIMATIONS_INFOS.keys():    raise ImportError("Animations differs")


COCO_NAMES = [
    "__background__",
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "N/A",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "N/A",
    "backpack",
    "umbrella",
    "N/A",
    "N/A",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "N/A",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "N/A",
    "dining table",
    "N/A",
    "N/A",
    "toilet",
    "N/A",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "N/A",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]
