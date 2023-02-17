from dronevis.drone_connect import nav_data_decode
import threading
import socket
import time
from typing import Callable

DATA_PORT = 5554
MAX_PACKET_SIZE = 1024 * 10


class Navdata(threading.Thread):
    "Manage the incoming data"

    def __init__(self, communication, callback=None) -> None:
        "Create the navdata handler thread"
        self.running = True
        self.port = DATA_PORT
        self.size = MAX_PACKET_SIZE
        self.com = communication
        self.ip = self.com.ip
        self.callback = callback
        self.f = nav_data_decode.navdata_decode
        self.last_drone_status = None
        self.socket_lock = threading.Lock()
        # Initialize the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0".encode(), self.port))
        self.sock.setblocking(False)
        threading.Thread.__init__(self)

    def change_callback(self, new_callback: Callable) -> bool:
        """Change the callback function

        Args:
            new_callback (function): new callback to be set

        Returns:
            bool: flag for valid callback exchange
        """
        # Check if the argument is a function
        if not hasattr(new_callback, "__call__"):
            return False
        self.callback = new_callback
        return True

    def run(self) -> None:
        "Start the data handler"
        self.com._activate_navdata(activate=True)  # Tell com thread that we are here
        # Initialize the drone to send the data
        self.sock.sendto("\x01\x00\x00\x00".encode(), (self.ip, self.port))
        time.sleep(0.05)
        while self.running:
            self.socket_lock.acquire()
            try:
                rep, client = self.sock.recvfrom(self.size)
            except socket.error:
                time.sleep(0.05)
            else:
                rep = self.f(rep)
                self.last_navdata = rep
                if rep["drone_state"]["command_ack"] == 1:
                    self.com._ack_command()
                assert self.callback, "Please set a callback"
                self.callback(rep)

            time.sleep(0.05)
            self.socket_lock.release()
        self.com._activate_navdata(activate=False)  # Tell com thread that we are out
        self.sock.close()

    def reconnect(self) -> bool:
        """Try to send another packet to reactivate navdata

        Returns:
            bool: flag for valid command communication
        """
        self.sock.sendto("\x01\x00\x00\x00".encode(), (self.ip, self.port))
        return True

    def stop(self) -> None:
        "Stop the communication"
        self.running = False
        time.sleep(0.05)
