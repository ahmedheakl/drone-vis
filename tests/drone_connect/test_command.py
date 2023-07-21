"""Test real drone command thread"""
import pytest

from dronevis.drone_connect.command import Command


@pytest.fixture
def command():
    """Fixture for getting a command thread instance"""
    cmd = Command()
    yield cmd
    del cmd


def test_init(command):
    """Test command thread initialization"""
    assert command.counter == 10
    assert command.com == ""
    assert not command.navdata_enabled
    assert not command.is_configured
    assert len(command.session_id) == 8
    assert len(command.profile_id) == 8
    assert len(command.app_id) == 8


def test_command(command):
    """Test command"""
    assert command.command("AT*REF\r")
    assert command.com == "AT*REF\r"


def test_ack_command(command):
    """Test ack command"""
    assert command.ack_command()
    assert command.thread_attr.ack


def test_activate_navdata(command):
    """Test activate navdata"""
    command.activate_navdata()
    assert command.navdata_enabled
    command.activate_navdata(False)
    assert not command.navdata_enabled


def test_stop(command):
    """Test stop"""
    assert command.stop()
    assert not command.thread_attr.running
