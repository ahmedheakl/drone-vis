"""Implementation for navigation data thread"""
from typing import Callable, Any, Dict
import threading
import socket
import time
import logging

from dronevis.drone_connect.navdata_decode import navdata_decode
from dronevis.drone_connect.command import Command

_LOG = logging.getLogger(__name__)


class Navdata(threading.Thread):
    "Manage the incoming data"
    data_port = 5554
    pocket_size = 1024 * 10

    def __init__(
        self,
        communication: Command,
        callback: Callable[[Dict[str, Dict[str, Any]]], None],
    ) -> None:
        "Create the navdata handler thread"
        super().__init__()
        self.running = True
        self.com = communication
        self.ip_address = self.com.thread_attr.ip_address
        self.callback = callback
        self.socket_lock = threading.Lock()
        # Initialize the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0".encode(), self.data_port))
        self.sock.setblocking(False)

    def change_callback(self, new_callback: Callable) -> bool:
        """Change the callback function

        Args:
            new_callback (function): new callback to be set

        Returns:
            bool: flag for valid callback exchange
        """
        # Check if the argument is a function
        if not hasattr(new_callback, "__call__"):
            _LOG.warning("Provided callback should be callable")
            return False
        self.callback = new_callback
        return True

    def run(self) -> None:
        """Start the data handler"""
        self.com.activate_navdata(activate=True)  # Tell com thread that we are here
        # Initialize the drone to send the data
        self.sock.sendto("\x01\x00\x00\x00".encode(), (self.ip_address, self.data_port))
        time.sleep(0.05)
        while self.running:
            with self.socket_lock:
                try:
                    rep, _ = self.sock.recvfrom(self.pocket_size)
                except socket.error:
                    time.sleep(0.05)
                else:
                    decoded_rep = navdata_decode(rep)
                    if decoded_rep["drone_state"]["command_ack"] == 1:
                        self.com.ack_command()
                    assert self.callback is None, "Please set a callback"
                    self.callback(decoded_rep)

                time.sleep(0.05)
        self.com.activate_navdata(activate=False)  # Tell com thread that we are out
        self.sock.close()

    def reconnect(self) -> bool:
        """Try to send another packet to reactivate navdata

        Returns:
            bool: flag for valid command communication
        """
        self.sock.sendto("\x01\x00\x00\x00".encode(), (self.ip_address, self.data_port))
        return True

    def stop(self) -> None:
        "Stop the communication"
        self.running = False
        time.sleep(0.05)
