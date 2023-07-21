"""Testing main script for running the GUI"""
import pytest

from dronevis.main_gui import main, DroneVisGui


def test_main_gui(monkeypatch, mocker) -> None:
    """Test main GUI"""
    gui_mock = mocker.Mock()
    monkeypatch.setattr("dronevis.main_gui.DroneVisGui", gui_mock)
    main(["--drone", "demo"])
    assert gui_mock.called


# def test_main_gui_with_keyboard_interrupt(monkeypatch, mocker) -> None:
#     """Test main GUI with keyboard interrupt"""
#     gui_mock = mocker.Mock()
#     monkeypatch.setattr("dronevis.main_gui.DroneVisGui", gui_mock)
#     gui_mock.side_effect = KeyboardInterrupt
#     with pytest.raises(SystemExit):
#         main(["--drone", "demo"])
#         assert gui_mock.called
