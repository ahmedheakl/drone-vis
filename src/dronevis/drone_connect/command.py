"""Implementation for the thread resposible for sending commands"""
import socket
import threading
import time
import random
import logging
from dataclasses import dataclass

_LOG = logging.getLogger(__name__)


@dataclass
class ThreadAttributes:
    """Attributes for each thread"""

    ip_address: str
    socket_lock: threading.Lock
    sock: socket.socket
    running: bool = False
    ack: bool = False


class Command(threading.Thread):
    """Command thread implementation for sending commands
    through a socket created between the drone and the sender.
    """

    command_port: int = 5556
    session_id = "".join(random.sample("0123456789abcdef", 8))
    profile_id = "".join(random.sample("0123456789abcdef", 8))
    app_id = "".join(random.sample("0123456789abcdef", 8))
    is_configured = False

    def __init__(self, ip: str = "192.168.1.1") -> None:
        """Initialize thread instance

        Args:
            ip (str, optional): ip of the drone. Defaults to "192.168.1.1".

        Raises:
            ConnectionError: raise an error if user is not connected to the drone
        """
        super().__init__()

        self.counter = 10  # Counter to issue AT command in order
        self.com = ""  # Last command to issue
        self.navdata_enabled = False  # If navdata is enabled or not (will check ACK)
        # Create the UDP Socket
        try:
            _LOG.info("Connecting to the Drone ...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect((ip, self.command_port))
            self.thread_attr = ThreadAttributes(
                ip_address=ip,
                running=True,
                socket_lock=threading.Lock(),
                ack=False,
                sock=sock,
            )
        except Exception as exc:
            error_message = (
                "Couldn't connect to the drone."
                + "Make sure you are connected to the drone network."
            )
            _LOG.critical(error_message)
            raise ConnectionError(error_message) from exc

        _LOG.info("Connected Successfully")

    # Usable commands
    def command(self, command: str = "") -> bool:
        """Send a command to the AR.Drone

        Args:
            command (str, optional): command string. Defaults to "".

        Returns:
            bool: flag for valid sequence of operations
        """
        self.com = command
        return True

    def configure(self, argument: str, value: str) -> bool:
        """Set a configuration onto the drone

        Args:
            argument (str): keys for configs
            value (str): values for configs

        Returns:
            bool: flag for valid config operations
        """
        # Check if it's the first time we send a config
        if not self.is_configured:
            # Activate the config
            self.is_configured = True
            self.configure("custom:session_id", self.session_id)
            time.sleep(1)  # Wait a lot in order for file to be created
            self.configure("custom:profile_id", self.profile_id)
            time.sleep(1)
            self.configure("custom:application_id", self.app_id)
            time.sleep(1)
        with self.thread_attr.socket_lock:
            if self.navdata_enabled:
                tries = 5
            else:
                tries = 0  # Only one try when no navdata (and wait)
            while tries >= 0:
                to_send = (
                    "AT*CONFIG_IDS="
                    + str(self.counter)
                    + ',"'
                    + self.session_id
                    + '","'
                    + self.profile_id
                    + '","'
                    + self.app_id
                    + '"\r'
                )
                self.thread_attr.sock.send(to_send.encode())
                if not self.navdata_enabled:
                    time.sleep(0.15)
                to_send = (
                    "AT*CONFIG="
                    + str(self.counter + 1)
                    + ',"'
                    + str(argument)
                    + '","'
                    + str(value)
                    + '"\r'
                )
                _LOG.debug(to_send)
                self.thread_attr.sock.send(to_send.encode())
                self.counter = self.counter + 2
                if self.navdata_enabled:  # Wait until we receive ACK if navadata enable
                    self.thread_attr.ack = False  # not acknoledged first
                    for _ in range(100):
                        if self.thread_attr.ack:
                            # print "OK"
                            break
                        time.sleep(0.5 / 100)  # Wait max 0.5 secs
                    if self.thread_attr.ack:
                        self.thread_attr.ack = False
                        break

                else:
                    time.sleep(
                        0.05
                    )  # But if we don't have navdata, just wait a fixed period
                tries -= 1
            navdata_command_str = "AT*CTRL=" + str(self.counter) + ",5,0"
            self.thread_attr.sock.send(navdata_command_str.encode())
            self.counter = self.counter + 1
        if tries >= 0 or not self.navdata_enabled:
            return True
        return False

    # Internal functions
    def ack_command(self) -> bool:
        """Call this function when the command is acknowledge

        Returns:
            bool: flag for valid ack
        """
        self.thread_attr.ack = True
        return True

    def activate_navdata(self, activate: bool = True) -> None:
        """Call this function when navdata are enabled

        Args:
            activate (bool, optional): whether to activate navdata. Defaults to True.
        """
        if activate:
            self.navdata_enabled = True
        else:
            self.navdata_enabled = False

    def run(self) -> None:
        """Send commands every 30ms"""
        while self.thread_attr.running:
            com = self.com
            # conf = self.continous_config
            with self.thread_attr.socket_lock:
                self.thread_attr.sock.send("AT*COMWDG\r".encode())
                if com is not None:
                    com = com.replace("#ID#", str(self.counter))
                    self.thread_attr.sock.send(com.encode())
                    self.counter += 1
            time.sleep(0.03)
        self.thread_attr.sock.close()

    def reconnect(self) -> None:
        """Try to restart the socket"""
        with self.thread_attr.socket_lock:
            self.thread_attr.sock.shutdown()  # type: ignore
            self.thread_attr.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.thread_attr.sock.connect(
                (self.thread_attr.ip_address, self.command_port)
            )

    def stop(self) -> bool:
        """Stop the communication

        Returns:
            bool: flag whether drone stopped corretly
        """
        self.thread_attr.running = False
        time.sleep(0.05)
        return True
