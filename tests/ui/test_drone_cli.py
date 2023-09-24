"""Testing dronevis cli"""
from unittest.mock import MagicMock, Mock
from typing import Generator
import pytest

from dronevis.ui.drone_cli import DroneCli
from dronevis.abstract.base_drone import BaseDrone


@pytest.fixture
def cli() -> Generator[DroneCli, None, None]:
    """Fixture to create a cli instance"""
    drone_cli = DroneCli()
    yield drone_cli
    del drone_cli


def test_parse(cli):
    """Testing cli parser"""
    args = cli.parse(["--drone", "real", "--log-level", "debug"])
    assert args.drone == "real"
    assert args.logger_level == "debug"


def test_parse_default(cli):
    """Testing cli parser with default values"""
    args = cli.parse([])
    assert args.drone == "demo"
    assert args.logger_level == "info"


def test_print_available_control(capsys):
    """Testing print available control"""
    drone_cli = DroneCli()
    drone_cli.print_available_control()
    captured = capsys.readouterr()
    output = captured.out
    assert "Control ID" in output
    assert "Task" in output
    assert "Status" in output


def test_index_to_control(cli):
    """Testing index to control"""
    mock_drone = MagicMock(spec=BaseDrone)
    expected_commands = {
        "1": pytest.approx(mock_drone.upward),
        "2": pytest.approx(mock_drone.downward),
        "3": pytest.approx(mock_drone.right),
        "4": pytest.approx(mock_drone.left),
        "5": pytest.approx(mock_drone.forward),
        "6": pytest.approx(mock_drone.backward),
        "7": pytest.approx(mock_drone.rotate_left),
        "8": pytest.approx(mock_drone.rotate_right),
        "9": pytest.approx(mock_drone.takeoff),
        "10": pytest.approx(mock_drone.land),
        "11": pytest.approx(mock_drone.hover),
        "12": pytest.approx(mock_drone.reset),
        "13": pytest.approx(mock_drone.emergency),
        "14": pytest.approx(cli._not_implemeneted),
    }
    for key, command in expected_commands.items():
        assert command == cli.index_to_control(mock_drone)[key]


def test_index_to_control_not_base_drone(cli):
    """Testing index to control with not implemented drone"""
    with pytest.raises(AssertionError):
        cli.index_to_control(Mock())


def test_not_implemented_method(cli):
    """Testing not implemented method"""
    with pytest.raises(NotImplementedError):
        cli._not_implemeneted()


def test_call_not_base_drone(cli):
    """Testing index to control with not implemented drone"""
    with pytest.raises(AssertionError):
        cli({}, Mock())
