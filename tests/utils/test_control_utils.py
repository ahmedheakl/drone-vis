"""Testing control utilities for drone"""
from typing import List, Tuple

import pytest

import dronevis.utils.control_utils as util


def test_activate_navdata_default():
    """Test activate_navdata"""
    assert util.activate_navdata() == [("general:navdata_demo", "FALSE")]


def test_activate_navdata_false():
    """Test activate_navdata"""
    assert util.activate_navdata(activate=False) == [("general:navdata_demo", "TRUE")]


def test_activate_navdata_true():
    """Test activate_navdata"""
    assert util.activate_navdata(activate=True) == [("general:navdata_demo", "FALSE")]


def test_activate_gps():
    """Test activate_gps"""
    assert util.activate_gps() == [
        ("control:flying_mode", "0"),
        ("control:autonomous_flight", "FALSE"),
    ]
    assert not util.activate_gps(False)


def test_detect_tag():
    """Test detect_tag"""
    # testing for blue-orange color
    assert util.detect_tag(0) == [
        ("detect:detect_type", "13"),
        ("detect:enemy_colors", "3"),
        ("detect:enemy_without_shell", "0"),
    ]

    # testing for yellow-orange color
    assert util.detect_tag(1) == [
        ("detect:detect_type", "13"),
        ("detect:enemy_colors", "2"),
        ("detect:enemy_without_shell", "0"),
    ]


def test_indoor_true():
    """Test indoor commands"""
    assert util.indoor() == [
        ("control:outdoor", "FALSE"),
        ("control:flight_without_shell", "FALSE"),
    ]


def test_indoor_false():
    """Test indoor commands"""
    assert util.indoor(False) == [
        ("control:outdoor", "TRUE"),
        ("control:flight_without_shell", "TRUE"),
    ]


def test_outdoor_true():
    """Test outdoor commands"""
    assert util.outdoor() == [
        ("control:outdoor", "TRUE"),
        ("control:flight_without_shell", "TRUE"),
    ]


def test_outdoor_false():
    """Test outdoor commands"""
    assert util.outdoor(False) == [
        ("control:outdoor", "FALSE"),
        ("control:flight_without_shell", "FALSE"),
    ]


def test_nervosity_level():
    """Test nervosity_level"""
    expected_output = [
        ("control:euler_angle_max", "0.1"),
        ("control:control_vz_max", "40000"),
        ("control:control_yaw", "1.22"),
    ]
    assert util.nervosity_level(20) == expected_output
    expected_output = [
        ("control:euler_angle_max", "0.52"),
        ("control:control_vz_max", "200000"),
        ("control:control_yaw", "6.11"),
    ]
    assert util.nervosity_level(100) == expected_output


def test_max_altitude():
    """Test max_altitude"""
    altitudes = [2, 5, 10]
    expected_results = [
        [("control:altitude_max", "2000")],
        [("control:altitude_max", "5000")],
        [("control:altitude_max", "10000")],
    ]

    for idx, altitude in enumerate(altitudes):
        assert util.max_altitude(altitude) == expected_results[idx]


def test_activate_video():
    """Test activate_video"""
    assert util.activate_video() == [("video:video_codec", "128")]
    assert not util.activate_video(False)


@pytest.mark.parametrize(
    "side, speed_expected",
    [
        ("LEFT", [("control:flight_anim", "18,15")]),
        ("RIGHT", [("control:flight_anim", "19,15")]),
        ("FRONT", [("control:flight_anim", "16,15")]),
        ("BACK", [("control:flight_anim", "17,15")]),
        ("left", [("control:flight_anim", "18,15")]),
        ("Right", [("control:flight_anim", "19,15")]),
        ("front", [("control:flight_anim", "16,15")]),
        ("back", [("control:flight_anim", "17,15")]),
        ("", [("control:flight_anim", "17,15")]),
    ],
)
def test_flip(side: str, speed_expected: List[Tuple[str, str]]):
    """Test flip"""
    assert util.flip(side) == speed_expected


def test_goto_gps_point():
    """Test goto_gps_point"""
    assert not util.goto_gps_point(0, 0)

    assert util.goto_gps_point(12.9716, 77.5946) == [
        ("control:flying_camera_enable", "FALSE"),
        ("control:flying_camera_mode", "10000,1500,129716000,775946000,2000,0,0,0,0,0"),
        ("control:flying_camera_enable", "TRUE"),
    ]

    assert util.goto_gps_point(32.7767, -96.7970, 100, 90) == [
        ("control:flying_camera_enable", "FALSE"),
        (
            "control:flying_camera_mode",
            "10000,1500,327767000,-967970000,100000,0,0,0,90,0",
        ),
        ("control:flying_camera_enable", "TRUE"),
    ]
    assert util.goto_gps_point(30.2669, -97.7428, 3.0, 20) == [
        ("control:flying_camera_enable", "FALSE"),
        (
            "control:flying_camera_mode",
            "10000,1500,302669000,-977428000,3000,0,0,0,20,0",
        ),
        ("control:flying_camera_enable", "TRUE"),
    ]
    assert util.goto_gps_point(30.2669, -97.7428, 3.0, 20, True) == [
        (
            "control:flying_camera_mode",
            "10000,1500,302669000,-977428000,3000,0,0,0,20,0",
        ),
    ]
