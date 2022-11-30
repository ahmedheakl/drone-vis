import socket
import threading
from dronevis.drone_connect.video import Video
from dronevis.drone_connect.command import Command
from dronevis.drone_connect.config import config
#from dronevis.drone_connect.navadata import Navdata
import struct
import time

class Drone():
    def __init__(self, ip = "192.168.1.1"):
        self.command_port = 5556
        self.data_port = 5554
        self.ip = ip

    def connect_video(self):
        self.video_thread = Video(self.ip)
        self.video_thread.start()
        #self.video_thread.run()


    def connect(self):
        try:
            self.comThread = Command(self.ip)
            self.c = self.comThread.command # Alias
            self.comThread.start()
        except:
            raise "connection error"
        
    def set_config(self,**args):
        """ Set a configuration onto the drone
            See possibles arguments with list_config"""
        # Check if all arguments are supported config
        for c in args.keys():
            print(c)
            if c.lower() not in config.SUPPORTED_CONFIG.keys():
                raise AttributeError("The configuration key "+str(c)+" can't be found!")
        # Then set each config
        at_commands = []
        for c in args.keys():
            at_commands = at_commands + config.SUPPORTED_CONFIG[c.lower()](args[c.lower()])
        for at in at_commands:
            self.comThread.configure(at[0],at[1])
        return True

    def list_config(self):
        "List all possible configuration"
        return list(config.SUPPORTED_CONFIG.keys())
    
    def takeoff(self):
        "Take Off"
        return self.c("AT*REF=#ID#," + str(self.bin2dec("00010001010101000000001000000000")) + "\r")

    def land(self):
        "Land"
        return self.c("AT*REF=#ID#," + str(self.bin2dec("00010001010101000000000000000000")) + "\r")

    def calibrate(self):
        "Calibrate sensors"
        return self.c("AT*FTRIM=#ID#\r")

    def forward(self,speed=0.2):
        "Make the drone go forward, speed is between 0 and 1"
        return self.navigate(front_back=-speed)

    def backward(self,speed=0.2):
        "Make the drone go backward, speed is between 0 and 1"
        return self.navigate(front_back=speed)

    def left(self,speed=0.2):
        "Make the drone go left, speed is between 0 and 1"
        return self.navigate(left_right=-speed)

    def up(self,speed=0.2):
        "Make the drone rise in the air, speed is between 0 and 1"
        return self.navigate(up_down=speed)

    def down(self,speed=0.2):
        "Make the drone descend, speed is between 0 and 1"
        return self.navigate(up_down=-speed)

    def rotate_left(self,speed=0.8):
        "Make the drone turn left, speed is between 0 and 1"
        return self.navigate(angle_change=-speed)

    def rotate_right(self,speed=0.8):
        "Make the drone turn right, speed is between 0 and 1"
        return self.navigate(angle_change=speed)

    def right(self,speed=0.2):
        "Make the drone go right, speed is between 0 and 1"
        return self.navigate(left_right=speed)

    def navigate(self, left_right=0, front_back=0, up_down=0, angle_change=0):
        "Command the drone, all the arguments are between -1 and 1"
        lr = self.float2dec(left_right)
        fb = self.float2dec(front_back)
        ud = self.float2dec(up_down)
        ac = self.float2dec(angle_change)
        return self.c("AT*PCMD=#ID#,1,"+str(lr)+","+str(fb)+","+str(ud)+","+str(ac)+"\r")
    def hover(self):
        "Make the drone stationary"
        return self.c("AT*PCMD=#ID#,0,0,0,0,0\r")

    def emergency(self):
        "Enter in emergency mode"
        # Release all lock to be sure command is issued
        return self.c("AT*REF=#ID#," + str(self.bin2dec("00010001010101000000000100000000")) + "\r")
    def stop(self):
        "Stop the AR.Drone"
        self.land()
        time.sleep(1)
        self.comThread.stop()

    def reset(self):
        "Reset the state of the drone"
        # Issue an emergency command
        self.emergency()
        time.sleep(0.5)
        # Then normal state
        return self.land()

    def bin2dec(self,bin):
        "Convert a binary number to an int"
        return int(bin,2)

    def float2dec(self,my_float):
        "Convert a python float to an int"
        return int(struct.unpack("=l",struct.pack("f",float(my_float)))[0])



