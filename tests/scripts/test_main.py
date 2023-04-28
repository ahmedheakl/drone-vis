"""Testing main cli"""
import sys
import unittest
import io
from unittest.mock import patch

from dronevis.__main__ import main, DroneCli, Drone


class TestMainCli(unittest.TestCase):
    """Testing main cli"""

    def test_main(self):
        """Testing main cli"""
        captured_output = io.StringIO()
        captured_error = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_error
        with patch.object(
            DroneCli,
            "__call__",
            side_effect=NotImplementedError,
        ) as mock_dronecli:
            arguments = ["--drone", "demo", "--log-level", "debug", "--mode", "cli"]
            main(arguments)
            assert mock_dronecli.call_count == 1
            output = captured_output.getvalue()
            err = captured_error.getvalue()
            assert "DroneVis CLI" in output
            assert "implemented" in err.lower()

    def test_main_connection_error(self):
        """Testing main cli with connection error"""
        captured_output = io.StringIO()
        captured_error = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_error
        with patch.object(
            DroneCli,
            "__call__",
            side_effect=ConnectionError,
        ) as mock_dronecli:
            arguments = ["--drone", "demo", "--log-level", "debug", "--mode", "cli"]
            main(arguments)
            assert mock_dronecli.call_count == 1
            output = captured_output.getvalue()
            err = captured_error.getvalue()
            assert "DroneVis CLI" in output
            assert "couldn't connect to the drone" in err.lower()

    def test_main_keyboard_interrupt(self):
        """Testing main cli with keyboard interrupt"""
        captured_output = io.StringIO()
        captured_error = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_error
        with patch.object(
            DroneCli,
            "__call__",
            side_effect=KeyboardInterrupt,
        ) as mock_dronecli:
            arguments = ["--drone", "demo", "--log-level", "debug", "--mode", "cli"]
            main(arguments)
            assert mock_dronecli.call_count == 1
            output = captured_output.getvalue()
            err = captured_error.getvalue()
            assert "DroneVis CLI" in output
            assert "drone disconnected" in err.lower()

    def test_main_value_error(self):
        """Testing main cli with value error"""
        captured_output = io.StringIO()
        captured_error = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_error
        with patch.object(
            DroneCli,
            "__call__",
            side_effect=ValueError,
        ) as mock_dronecli:
            arguments = ["--drone", "demo", "--log-level", "debug", "--mode", "cli"]
            main(arguments)
            assert mock_dronecli.call_count == 1
            output = captured_output.getvalue()
            err = captured_error.getvalue()
            assert "DroneVis CLI" in output
            assert "an error occured" in err.lower()

    def test_main_with_real_drone(self):
        """Testing main cli with real drone"""
        captured_output = io.StringIO()
        captured_error = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_error
        with patch.object(
            DroneCli,
            "__call__",
            side_effect=NotImplementedError,
        ) as mock_dronecli:
            with patch.object(Drone, "connect", return_value=True) as mock_drone:
                arguments = ["--drone", "real", "--log-level", "debug", "--mode", "cli"]
                main(arguments)
                output = captured_output.getvalue()
                err = captured_error.getvalue()
                assert mock_dronecli.call_count == 1
                assert mock_drone.connect.called_once()
                assert "DroneVis CLI" in output
                assert "implemented" in err.lower()
