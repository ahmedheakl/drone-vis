"""Utilities for controling the drone"""
from typing import List, Tuple


def activate_navdata(activate: bool = True) -> List[Tuple[str, str]]:
    "Prepare the drone so he can send navdata back to us"
    if activate:
        return [("general:navdata_demo", "FALSE")]  # Activate navdata
    return [("general:navdata_demo", "TRUE")]


def activate_gps(activate: bool = True) -> List[Tuple[str, str]]:
    "Prepare the drone to receive GPS command"
    if activate:
        return [("control:flying_mode", "0"), ("control:autonomous_flight", "FALSE")]
    return []


def detect_tag(color: int = 0) -> List[Tuple[str, str]]:
    """Send the config to the drone to activate drone detection
    0 is the blue-orange color
    1 is the yellow-orange color"""
    if color == 1:
        tag_color = "2"
    else:
        tag_color = "3"
    com = []
    com.append(("detect:detect_type", "13"))
    com.append(("detect:enemy_colors", tag_color))
    com.append(("detect:enemy_without_shell", "0"))
    return com


# ONE-TIME CONFIG RELATED
def indoor(activate: bool = True) -> List[Tuple[str, str]]:
    "Set the drone config to act as if it is indoor"
    if activate:
        return [("control:outdoor", "FALSE"), ("control:flight_without_shell", "FALSE")]
    return outdoor(activate=True)


def outdoor(activate: bool = True) -> List[Tuple[str, str]]:
    "Set the drone config to act as if it is outdoor"
    if activate:
        return [("control:outdoor", "TRUE"), ("control:flight_without_shell", "TRUE")]
    return indoor(activate=True)


def nervosity_level(percentage: int = 20) -> List[Tuple[str, str]]:
    """Configure the nervosity of the drone,percentage=10:weak
    response to command; percentage=100:full trust"""
    euler = int(0.52 * percentage) / 100.0  # 2 digits after coma
    vertical_speed = int(2000 * percentage)
    yaw = int(6.11 * percentage) / 100.0
    com = []
    com.append(("control:euler_angle_max", str(euler)))
    com.append(("control:control_vz_max", str(vertical_speed)))
    com.append(("control:control_yaw", str(yaw)))
    return com


def max_altitude(altitude: int = 5) -> List[Tuple[str, str]]:
    "Set the max altitude of the drone"
    return [("control:altitude_max", str(int(altitude * 1000)))]


def activate_video(activate=True) -> List[Tuple[str, str]]:
    "Start/Stop the recording of a video on the USB key"
    if activate:
        return [("video:video_codec", "128")]
    return []


# Animations
def flip(side: str = "LEFT") -> List[Tuple[str, str]]:
    """Do a flip, side is the side of the flip
    Side is LEFT, RIGHT, FRONT, BACK"""
    side_speed = 17
    if side.upper() == "FRONT":
        side_speed = 16
    elif side.upper() == "LEFT":
        side_speed = 18
    elif side.upper() == "RIGHT":
        side_speed = 19
    return [("control:flight_anim", str(side_speed) + ",15")]


# Autonomous Flight
def goto_gps_point(
    latitude: float,
    longitude: float,
    altitude: float = 2.0,
    cap: float = 0.0,
    continuous: bool = False,
) -> List[Tuple[str, str]]:
    "Send the drone to the GPS point, cap is in degre"
    if (longitude == 0) or (latitude == 0):
        return []  # Try not to send drone to somewhere weird
    # Compute each data
    longi = int(longitude * 10000000)
    lati = int(latitude * 10000000)
    alt = int(altitude * 1000)
    cap = int(cap)
    # Create the right parameter according to doc
    param1 = (
        "10000,1500,"
        + str(lati)
        + ","
        + str(longi)
        + ","
        + str(alt)
        + ",0,0,0,"
        + str(cap)
        + ",0"
    )
    com = []
    if not continuous:
        com.append(("control:flying_camera_enable", "FALSE"))
    com.append(("control:flying_camera_mode", param1))
    if not continuous:
        com.append(("control:flying_camera_enable", "TRUE"))
    return com
