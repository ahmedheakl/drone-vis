"""Implementation for real drone control"""
from typing import Callable, Optional, List, Tuple
import logging
import struct
import time
import socket

from dronevis.abstract.base_drone import BaseDrone
from dronevis.drone_connect.video import VideoThread
from dronevis.drone_connect.command import Command
from dronevis.drone_connect.navdata import Navdata
from dronevis.config import general as cfg

_LOG = logging.getLogger(__name__)


class Drone(BaseDrone):
    """Drone implementation for connecting, controlling, retrieving video
    stream from the drone using sockets"""

    command_port = 5556
    data_port = 5554

    def __init__(self, ip_address: str = "192.168.1.1") -> None:
        """Initialize ip and communication ports

        Args:
            ip_address (str, optional): IP of the drone. Defaults to "192.168.1.1".
        """
        super().__init__(ip_address)
        self.video_thread: Optional[VideoThread] = None
        self.com_thread: Optional[Command] = None
        self.nav_thread: Optional[Navdata] = None
        self.com: Optional[Callable[[str], bool]] = None

    def connect_video(
        self,
        close_callback: Callable,
        operation_callback: Callable,
        model_name: str,
    ) -> None:
        """Initialize and start video thread

        Args:
            close_callback (Callable): Callback to be invoked after closing the video thread
            model_name (str): Computer vision to run over the video stream
            operation_callback (Callable): Callback to be invoked after each operation

        Raises:
            TypeError: Provided callback should be callable
        """

        super().connect_video(close_callback, operation_callback, model_name)

        self.video_thread = VideoThread(
            close_callback,
            operation_callback,
            model_name,
            self.ip_address,
        )
        self.video_thread.resume()
        _LOG.debug("Initialized video thread")

    def disconnect_video(self) -> None:
        """Disconnect video stream"""
        if self.video_thread is None:
            _LOG.warning("Video thread is not initialized")
            return

        self.video_thread.stop()
        _LOG.debug("Disconnected video thread")

    def connect(self) -> None:
        """Start communication thread to send control commands

        Raises:
            ConnectionError: Lost connection to drone
            ConnectionError: Cannot send commands to drone
        """
        if not self._check_telnet():
            err_message = (
                "Couldn't connect to the drone."
                + "Make sure you are connected to the drone network."
            )
            _LOG.critical(err_message)
            raise ConnectionError(err_message)
        try:
            self.com_thread = Command(self.ip_address)
            self.com = self.com_thread.command  # Alias
            self.com_thread.start()
            self.is_connected = True
            self.nav_thread = None

        except Exception as exc:
            err_message = (
                "Couldn't connect to the drone."
                + "Make sure you are connected to the drone network."
            )
            _LOG.critical(err_message)
            raise ConnectionError(err_message) from exc

    def set_config(self, **kwargs: bool) -> bool:
        """Set a configuration onto the drone

        See possibles arguments with ```list_config```

        Raises:
            AttributeError: raised when there is an invalid config

        Returns:
            bool: a flag that everything went fine
        """
        assert self.com_thread, "Please connect to the drone first"

        # Check if all arguments are supported config
        for key_arg in kwargs:
            _LOG.debug(key_arg)
            if key_arg.lower() not in list(cfg.SUPPORTED_CONFIG):
                err_message = f"The configuration key {key_arg} can't be found!"
                _LOG.critical(err_message)
                raise AttributeError(err_message)
        # Then set each config
        at_commands: List[Tuple[str, str]] = []
        for key_arg in kwargs:
            config_out = cfg.SUPPORTED_CONFIG[key_arg.lower()](kwargs[key_arg.lower()])
            at_commands.extend(config_out)
        for at_command in at_commands:
            self.com_thread.configure(at_command[0], at_command[1])
        return True

    def list_config(self) -> list:
        """List all possible configuration

        Returns:
            list: list of configurations
        """
        return list(cfg.SUPPORTED_CONFIG.keys())

    def takeoff(self) -> bool:
        """Take Off

        Returns:
            bool: a flag for valid execution
        """
        assert self.com, "Please connect to the drone first"
        return self.com(
            "AT*REF=#ID#,"
            + str(self._bin2dec("00010001010101000000001000000000"))
            + "\r"
        )

    def land(self) -> bool:
        """Land

        Returns:
            bool: a flag for valid execution
        """
        assert self.com, "Please connect to the drone first"
        return self.com(
            "AT*REF=#ID#,"
            + str(self._bin2dec("00010001010101000000000000000000"))
            + "\r"
        )

    def calibrate(self) -> bool:
        """Calibrate sensors

        Returns:
            bool: a flag for valid execution
        """
        assert self.com, "Please connect to the drone first"
        return self.com("AT*FTRIM=#ID#\r")

    def forward(self, speed: float = 0.2) -> bool:
        """Make the drone go forward, speed is between 0 and 1

        Args:
            speed (float, optional): speed of the forward move. Defaults to 0.2.

        Returns:
            bool: a flag for valid execution
        """
        return self.navigate(front_back=-speed)

    def backward(self, speed: float = 0.2) -> bool:
        """Make the drone go backward, speed is between 0 and 1

        Args:
            speed (float, optional): speed of back move. Defaults to 0.2.

        Returns:
            bool: a flag for valid execution
        """
        return self.navigate(front_back=speed)

    def left(self, speed: float = 0.2) -> bool:
        """Make the drone go left, speed is between 0 and 1

        Args:
            speed (float, optional): speed of left move. Defaults to 0.2.

        Returns:
            bool: a flag for valid execution
        """
        return self.navigate(left_right=-speed)

    def upward(self, speed: float = 0.2) -> bool:
        """Make the drone rise in the air, speed is between 0 and 1

        Args:
            speed (float, optional): speed of right move. Defaults to 0.2.

        Returns:
            bool: a flag for valid execution
        """
        return self.navigate(up_down=speed)

    def downward(self, speed: float = 0.2) -> bool:
        """Make the drone descend, speed is between 0 and 1

        Args:
            speed (float, optional): speed of down move. Defaults to 0.2.

        Returns:
            bool: a flag for valid execution
        """
        return self.navigate(up_down=-speed)

    def rotate_left(self, speed: float = 0.8) -> bool:
        """Make the drone turn left, speed is between 0 and 1

        Args:
            speed (float, optional): speed of rotation. Defaults to 0.8.

        Returns:
            bool: a flag for valid execution
        """
        return self.navigate(angle_change=-speed)

    def rotate_right(self, speed: float = 0.8) -> bool:
        """Make the drone turn right, speed is between 0 and 1

        Args:
            speed (float, optional): speed of rotation. Defaults to 0.8.

        Returns:
            bool: a flag for valid execution
        """
        return self.navigate(angle_change=speed)

    def right(self, speed: float = 0.2) -> bool:
        """Make the drone go right, speed is between 0 and 1

        Args:
            speed (float, optional): speed of rotation. Defaults to 0.2.

        Returns:
            bool: a flag for valid execution
        """
        return self.navigate(left_right=speed)

    def navigate(
        self,
        left_right: float = 0.0,
        front_back: float = 0.0,
        up_down: float = 0.0,
        angle_change: float = 0.0,
    ) -> bool:
        """Command the drone, all the arguments are between -1 and 1

        Args:
            left_right (int, optional): how much horizontal move (y-axis). Defaults to 0.
            front_back (int, optional): how much horizontal move (x-axis). Defaults to 0.
            up_down (int, optional): how much vertical move (z-axis). Defaults to 0.
            angle_change (int, optional): how much to change the angle. Defaults to 0.

        Returns:
            bool: a flag for valid execution
        """
        left_right_dec = self._float2dec(left_right)
        forward_back_dec = self._float2dec(front_back)
        up_down_dec = self._float2dec(up_down)
        angle_change_dec = self._float2dec(angle_change)

        assert self.com, "Please connect to the drone first"
        return self.com(
            "AT*PCMD=#ID#,1,"
            + str(left_right_dec)
            + ","
            + str(forward_back_dec)
            + ","
            + str(up_down_dec)
            + ","
            + str(angle_change_dec)
            + "\r"
        )

    def hover(self) -> bool:
        """Make the drone stationary

        Returns:
            bool: a flag for valid execution
        """
        assert self.com, "Please connect to the drone first"
        return self.com("AT*PCMD=#ID#,0,0,0,0,0\r")

    def emergency(self) -> bool:
        """Enter in emergency mode

        Returns:
           str: a flag for valid execution
        """
        # Release all lock to be sure command is issued
        assert self.com, "Please connect to the drone first"
        return self.com(
            "AT*REF=#ID#,"
            + str(self._bin2dec("00010001010101000000000100000000"))
            + "\r"
        )

    def stop(self) -> None:
        """Stop the drone"""
        self.is_connected = False
        if self.com_thread is not None:
            self.land()
            time.sleep(1)
            self.com_thread.stop()

        if self.nav_thread is not None:
            self.nav_thread.stop()
            self.nav_thread.join()

        if self.video_thread is not None:
            self.video_thread.close_thread()
            self.video_thread.join()

    def set_callback(self, callback=None):
        "Set the callback function"
        # Check if the argument is a function
        if callback is None:
            callback = self._print_navdata

        if not hasattr(callback, "__call__"):
            err_message = "Callaback provided should be a function"
            _LOG.critical(err_message)
            raise TypeError(err_message)

        if self.nav_thread is None:
            assert self.com_thread, "Communication thread should be initialized first"
            # Initialize the navdata thread and navdata
            self.nav_thread = Navdata(self.com_thread, callback)
            # self.set_config(activate_navdata=True)
            self.nav_thread.start()

        else:
            self.nav_thread.change_callback(callback)
            self.nav_thread.start()

    def _print_navdata(self, data: dict) -> None:
        """Print navigation data to console
        Should be invoked as a callback

        Args:
            data (dict): Navigation data to be printed
        """
        print(data)

    def reset(self) -> bool:
        """Reset the state of the drone

        Returns:
            bool: a flag for valid execution
        """
        # Issue an emergency command
        self.emergency()
        time.sleep(0.5)
        # Then normal state
        return self.land()

    def _bin2dec(self, binay_str: str) -> int:
        """Convert a binary number to an int

        Args:
            bin (str): binary string

        Returns:
            int: value of the result integer
        """
        return int(binay_str, 2)

    def _float2dec(self, my_float: float) -> int:
        """Convert a python float to an int

        Args:
            my_float (float): input float

        Returns:
            int: value of the result integer
        """
        return int(struct.unpack("=l", struct.pack("f", float(my_float)))[0])

    def _check_telnet(self) -> bool:
        """Check if we can connect to telnet

        Returns:
            bool: flag whether there is a valid connection
        """
        sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_port = 23
        try:
            sock.connect((self.ip_address, connection_port))
        except ConnectionError as _:
            _LOG.critical("No drone connection")
            return False
        sock.close()
        return True
