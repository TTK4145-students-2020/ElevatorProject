import socket
from multiprocessing import Process, SimpleQueue
from threading import Thread

# UDP_IP = "localhost"
# UDP_PORT = 55681
class Network:
    count = 0
    def __init__(self, IP_address, port):
    #Sets the broadcasting settings and connect.
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.sock.bind(("", port))
            self.sock.settimeout(3)
        except:
            pass 
            
    #def connect_node(self, IP_address, port):
    #This function make a connection with another.
        
    def disconnect_node(self):     
    # Disconnects a connection.
        self.sock.shutdown()
        self.sock.close()

    def UDP_broadcast(self, json_packet, IP_address, port):
    # Broadcaster given packet to network.
        self.sock.sendto(json_packet, (IP_address,port))

    def UDP_listen(self, port):
    # Listens given port all the time.
        json_packet, address = self.sock.recvfrom(1024)
    
        return json_packet, address


