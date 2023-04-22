"""Testing drone packet decode"""
from typing import Dict
from dronevis.drone_connect.navdata_decode import (
    _drone_status_decode,
    _navdata_demo_decode,
)


def test_drone_status_decode():
    packet = 2
    expected_output = {
        "flying": 0,
        "video_on": 1,
        "vision_on": 0,
        "angle_algo": 0,
        "altitude_algo": 0,
        "user_feedback": 0,
        "command_ack": 0,
        "fw_ok": 0,
        "fw_new": 0,
        "fw_update": 0,
        "navdata_demo": 0,
        "navdata_bootstrap": 0,
        "motor_status": 0,
        "com_lost": 0,
        "vbat_low": 0,
        "user_emergency": 0,
        "timer_elapsed": 0,
        "too_much_angle": 0,
        "ultrasound_ok": 0,
        "cutout": 0,
        "pic_version_ok": 0,
        "atcodec_thread_on": 0,
        "navdata_thread_on": 0,
        "video_thread_on": 0,
        "acq_thread_on": 0,
        "ctrl_watchdog": 0,
        "adc_watchdog": 0,
        "com_watchdog": 0,
        "emergency": 0,
    }

    result = _drone_status_decode(packet)

    assert result == expected_output
