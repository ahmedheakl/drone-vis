import socket
import threading
from dronevis.drone_connect.config import config
import time
import random

class Command(threading.Thread):
    """

    """
    def __init__(self, ip = "192.168.1.1"):
        "Create the Command Thread"
        self.running = True
        self.ip = ip
        self.command_port = 5556        
        self.counter = 10 # Counter to issue AT command in order
        self.com = None # Last command to issue
        self.socket_lock = threading.Lock() # Create the lock for the socket
        self.navdata_enabled = False # If navdata is enabled or not (will check ACK)
        self.ack = False
        # Create the UDP Socket
        try:
            print("connecting to the Drone.............")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.connect((self.ip, self.command_port))
        except:
            raise "Connection Error"

        print("Connected Sucsuffly")
        self.session_id =   "".join(random.sample("0123456789abcdef",8))
        self.profile_id =   "".join(random.sample("0123456789abcdef",8))
        self.app_id =       "".join(random.sample("0123456789abcdef",8))
        self.is_configurated = False
        threading.Thread.__init__(self)
    
    # Usable commands
    def command(self,command=None):
        "Send a command to the AR.Drone"
        self.com = command
        return True
    
    def configure(self, argument, value):
        "Set a configuration onto the drone"
        # Check if it's the first time we send a config
        DEBUG = True
        if not self.is_configurated:
            # Activate the config
            self.is_configurated = True
            self.configure("custom:session_id",self.session_id)
            time.sleep(1) # Wait a lot in order for file to be created
            self.configure("custom:profile_id",self.profile_id)
            time.sleep(1)
            self.configure("custom:application_id",self.app_id)
            time.sleep(1)
        self.socket_lock.acquire()
        if self.navdata_enabled:
             tries = 5
        else:
            tries=0     # Only one try when no navdata (and wait)
        while tries >= 0:
            to_send = "AT*CONFIG_IDS="+str(self.counter) + ',"' + self.session_id + '","' + self.profile_id + '","' + self.app_id + '"\r'
            self.sock.send(to_send.encode())
            if not self.navdata_enabled:
                time.sleep(0.15)
            to_send = "AT*CONFIG="+str(self.counter+1)+',"' + str(argument) + '","' + str(value) + '"\r'
            if DEBUG:
                print(to_send) # Printing the AT*CONFIG we are sending
            self.sock.send(to_send.encode())
            self.counter = self.counter + 2
            if self.navdata_enabled:    # Wait until we receive ACK if navadata enable
                ack = False # not acknoledged first
                for i in range(100):
                    if self.__ack:
                        #print "OK"
                        break
                    time.sleep(0.5/100) # Wait max 0.5 secs
                if self.__ack:
                    self.__ack = False
                    break
                    
            
            else:
                time.sleep(0.05)    # But if we don't have navdata, just wait a fixed period
            tries -= 1
        x="AT*CTRL="+str(self.counter)+",5,0"
        self.sock.send(x.encode())
        self.counter = self.counter + 1
        self.socket_lock.release()
        if tries >= 0 or not self.navdata_enabled:  return True
        else:                                       return False
    # Internal functions
    def _ack_command(self):
        "Call this function when the command is acknoledge"
        self.__ack = True
        return True
    def _activate_navdata(self,activate=True):
        "Call this function when navdata are enabled"
        if activate:
            self.navdata_enabled = True
        else:
            self.navdata_enabled = False
    
    def run(self):
        "Send commands every 30ms"
        while self.running:
            com = self.com
            #conf = self.continous_config
            self.socket_lock.acquire() # Ask for the permission to send msg
            self.sock.send("AT*COMWDG\r".encode())
            if com != None:
                com = com.replace("#ID#",str(self.counter))
                self.sock.send(com.encode())
                self.counter += 1
            self.socket_lock.release()
            time.sleep(0.03)
        self.sock.close()
    def reconnect(self):
        "Try to restart the socket"
        self.socket_lock.acquire()
        self.sock.shutdown()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.ip, self.port))
        self.socket_lock.release()
        
    def stop(self):
        "Stop the communication"
        self.running = False
        time.sleep(0.05)
        return True
