from dronevis.drone_connect import nav_data_decode
import threading
import socket
import time
DATA_PORT = 5554
MAX_PACKET_SIZE = 1024 * 10
class Navdata(threading.Thread):
    "Manage the incoming data"
    def __init__(self, communication, callback = None):
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
        self.sock.bind(('0.0.0.0'.encode(),self.port))
        self.sock.setblocking(0)
        threading.Thread.__init__(self)
        
    def change_callback(self, new_callback):
        "Change the callback function"
        # Check if the argument is a function
        if not hasattr(new_callback, '__call__'):   return False
        self.callback = new_callback
        return True

    def run(self):
        "Start the data handler"
        self.com._activate_navdata(activate=True) # Tell com thread that we are here
        # Initialize the drone to send the data
        self.sock.sendto("\x01\x00\x00\x00".encode(), (self.ip,self.port))
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
                if rep["drone_state"]['command_ack'] == 1:
                    self.com._ack_command()
                
                self.callback(rep)

            time.sleep(0.05)
            self.socket_lock.release()       
        self.com._activate_navdata(activate=False) # Tell com thread that we are out
        self.sock.close()


    def reconnect(self):
        "Try to send another packet to reactivate navdata"
        self.sock.sendto("\x01\x00\x00\x00".encode(), (self.ip,self.port))
        return True
        
    def stop(self):
        "Stop the communication"
        self.running = False
        time.sleep(0.05)