from typing import Literal
from dronevis.drone_connect.video import Video
from dronevis.drone_connect.command import Command
from dronevis.drone_connect.navdata import Navdata
from dronevis.config import config
import struct
import time
import threading
import socket


class Drone():
    def __init__(self, ip="192.168.1.1", model=None) -> None:
        """Initialize ip and communication ports
        
        Args:
            ip (str, optional): IP of the drone. Defaults to "192.168.1.1".
        """
        self.command_port = 5556
        self.data_port = 5554
        self.ip = ip
        self.is_connected = False
        self.model = model

    def connect_video(self) -> None:
        self.video_thread = Video(self.ip, self.model)
        self.video_thread.start()
        

    def connect(self) -> None:
        """Start communication thread to send control commands"""
        if not self.check_telnet():
            raise ConnectionError(
                "Couldn't connect to the drone. Make sure you are connected to the drone network."
            )
        try:
            
            self.comThread = Command(self.ip)
            self.c = self.comThread.command  # Alias
            self.comThread.start()
            self.is_connected = True
            self.navThread = None
        except:
            raise ConnectionError(
                "Couldn't connect to the drone. Make sure you are connected to the drone network."
            )

    def set_config(self, **args) -> bool:
        """Set a configuration onto the drone
        
        See possibles arguments with ```list_config```
        Raises:
            AttributeError: raised when there is an invalid config
        Returns:
            bool: a flag that everything went fine
        """
        # Check if all arguments are supported config
        for c in args.keys():
            print(c)
            if c.lower() not in config.SUPPORTED_CONFIG.keys():
                raise AttributeError(
                    "The configuration key " + str(c) + " can't be found!"
                )
        # Then set each config
        at_commands = []
        for c in args.keys():
            at_commands = at_commands + config.SUPPORTED_CONFIG[c.lower()](
                args[c.lower()]
            )
        for at in at_commands:
            self.comThread.configure(at[0], at[1])
        return True

    def list_config(self) -> list:
        """List all possible configuration
        
        Returns:
            list: list of configurations
        """
        return list(config.SUPPORTED_CONFIG.keys())

    def takeoff(self) -> bool:
        """Take Off
        
        Returns:
            bool: a flag for valid execution
        """
        return self.c(
            "AT*REF=#ID#,"
            + str(self.bin2dec("00010001010101000000001000000000"))
            + "\r"
        )

    def land(self) -> bool:
        """Land
        
        Returns:
            bool: a flag for valid execution
        """
        return self.c(
            "AT*REF=#ID#,"
            + str(self.bin2dec("00010001010101000000000000000000"))
            + "\r"
        )

    def calibrate(self) -> bool:
        """Calibrate sensors
        
        Returns:
            bool: a flag for valid execution
        """
        return self.c("AT*FTRIM=#ID#\r")

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

    def up(self, speed: float = 0.2) -> bool:
        """Make the drone rise in the air, speed is between 0 and 1
        
        Args:
            speed (float, optional): speed of right move. Defaults to 0.2.
        Returns:
            bool: a flag for valid execution
        """
        return self.navigate(up_down=speed)

    def down(self, speed: float = 0.2) -> bool:
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
        left_right: float = 0,
        front_back: float = 0,
        up_down: float = 0,
        angle_change: float = 0,
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
        lr = self.float2dec(left_right)
        fb = self.float2dec(front_back)
        ud = self.float2dec(up_down)
        ac = self.float2dec(angle_change)
        return self.c(
            "AT*PCMD=#ID#,1,"
            + str(lr)
            + ","
            + str(fb)
            + ","
            + str(ud)
            + ","
            + str(ac)
            + "\r"
        )

    def hover(self) -> bool:
        """Make the drone stationary
        
        Returns:
            bool: a flag for valid execution
        """
        return self.c("AT*PCMD=#ID#,0,0,0,0,0\r")

    def emergency(self) -> bool:
        """Enter in emergency mode
        
        Returns:
           str: a flag for valid execution
        """
        # Release all lock to be sure command is issued
        return self.c(
            "AT*REF=#ID#,"
            + str(self.bin2dec("00010001010101000000000100000000"))
            + "\r"
        )

    def stop(self):
        """Stop the drone"""
        self.land()
        time.sleep(1)
        self.comThread.stop()
        if self.navThread is not None:
            self.navThread.stop()

    def set_callback(self, callback = None):
        "Set the callback function"
        # Check if the argument is a function
        if callback == None:
            callback = self.print_navdata
        if not hasattr(callback, '__call__'):   raise TypeError("Need a function")
        if self.navThread == None:
            # Initialize the navdata thread and navdata
            self.navThread = Navdata(self.comThread, callback)
            #self.set_config(activate_navdata=True)
            self.navThread.start()
            
        else:
            self.navThread.change_callback(callback)
            self.navThread.start()

    def print_navdata(self,data):
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

    def bin2dec(self, bin: str) -> int:
        """Convert a binary number to an int
        
        Args:
            bin (str): binary string
        Returns:
            int: value of the result integer
        """
        return int(bin, 2)

    def float2dec(self, my_float: float) -> int:
        """Convert a python float to an int
        
        Args:
            my_float (float): input float
        Returns:
            int: value of the result integer
        """
        return int(struct.unpack("=l", struct.pack("f", float(my_float)))[0])

    def check_telnet(self) -> bool:
        """Check if we can connect to telnet
        
        Returns:
            bool: flag whether there is a valid connection
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_port = 23
        try:
            sock.connect((self.ip, connection_port))
        except:
            return False
        else:
            sock.close()
            return True