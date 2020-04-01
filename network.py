import socket
import config
#from multiprocessing import Process, SimpleQueue
from threading import Thread
import fsm
import order



class Network:
    online_elevators = [0]*config.N_ELEVATORS
    def __init__(self, ID): #IP_address, port,
    #Sets the broadcasting settings and connect
        try:
            
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            

        except:
            pass 
        self.ID = ID
        self.sock.settimeout(3)
        Network.online_elevators[ID] = 1
            
    #def connect_node(self, IP_address, port):
    #This function make a connection with another.
        
    def disconnect_node(self, port):     
    # Disconnects a connection.
        Network.online_elevators[self.ID] = 0
        self.sock.shutdown()
        self.sock.close()

    def UDP_broadcast(self, json_packet, IP_address, port):
    # Broadcaster given packet to network.
        try:
            for i in range(10):
                self.sock.sendto(json_packet, (IP_address,port))
        except socket.timeout:
            print("error")

    def UDP_listen(self, port):
    # Listens given port.
        try:
            self.sock.bind(("", port))
        except:
            pass
        try:
            json_packet, address = self.sock.recvfrom(1024)
            json_packet = json_packet.decode(encoding="ascii")

            return json_packet, address
        except socket.timeout:
            return port
        #except:
         #   return port
        
    def msg_receive_handler(self):
        
        while True:

            for i in range(config.N_ELEVATORS):
                if(i != config.ELEV_ID):
                    msg = self.UDP_listen(config.BASE_ELEVATOR_PORT+i)
                    if(isinstance(msg, int) == 0):
                        Network.online_elevators[i] = 1
                        try:
                            print("halla")
                            position_matrix = fsm.Fsm.queue.order_json_decode_position_matrix(msg[0])
                            for j in range (config.N_FLOORS):
                                fsm.Fsm.m_position_matrix[j][i] = position_matrix[j][i]
                        except:
                            pass
                        try:
                            print("hei")
                            order_matrix = fsm.Fsm.queue.order_json_decode_order_matrix(msg[0])
                            for j in range (config.N_FLOORS):
                                fsm.Fsm.m_position_matrix[j][i] = position_matrix[j][i]
                        except:
                            pass
                        if(msg[0] != "alive"):
                            self.UDP_broadcast(bytes("alive","ascii"), "", config.BASE_ELEVATOR_PORT+config.ELEV_ID)                            
                    else:
                        Network.online_elevators[msg-config.BASE_ELEVATOR_PORT] = 0

    def msg_send_handler(self):
        while True:
            pass
            #if(fsm.Fsm.queue.order_poll_buttons()):
                #print("sender")
                #self.UDP_broadcast(bytes(fsm.encoded_order_matrix, "ascii"), "", config.BASE_ELEVATOR_PORT+config.ELEV_ID)
            #if(fsm.Fsm.fsm_get_current_floor() != -1 and fsm.Fsm.m_prev_registered_floor != fsm.Fsm.fsm_get_current_floor()):
                #print("sender bøsss")
                #self.UDP_broadcast(bytes(encoded_order_matrix, "ascii"), "", config.BASE_ELEVATOR_PORT+config.ELEV_ID)



################################################# alt under tør jeg ikke å slette enda, men det er i utgangspunktet søppel
    def update_order_matrix(self, encoded_order_matrix):
        for i in range(10):
            self.UDP_broadcast(bytes(encoded_order_matrix, "ascii"), "", config.BASE_ELEVATOR_PORT+config.ELEV_ID)

        for i in range(config.N_ELEVATORS):
            if(i != config.ELEV_ID):
                msg = self.UDP_listen(config.BASE_ELEVATOR_PORT+i)
                if(isinstance(msg, int) == 0):
                    #recieved_response += 1
                    Network.online_elevators[i] = 1
                    #position_matrix = fsm.Fsm.queue.order_json_decode_position_matrix()
                    #order_matrix = fsm.Fsm.queue.order_json_decode_order_matrix(msg[0])
                    #for j in range(config.N_FLOORS):
                    #    fsm.Fsm.queue.m_order_matrix[j][i] = order_matrix[j][i]
                else:
                    #recieved_response += 1
                    Network.online_elevators[msg-config.BASE_ELEVATOR_PORT] = 0

    def update_pos_matrix(self, encoded_pos_matrix):
        for i in range(10):
            self.UDP_broadcast(bytes(encoded_pos_matrix, "ascii"), "", config.BASE_ELEVATOR_PORT+config.ELEV_ID)
        
        for i in range(config.N_ELEVATORS):
            if(i != config.ELEV_ID):
                msg = self.UDP_listen(config.BASE_ELEVATOR_PORT+i)

                if(isinstance(msg, int) == 0):
                    Network.online_elevators[i] = 1
                else:
                    Network.online_elevators[msg-config.BASE_ELEVATOR_PORT] = 0


    def update_order_and_pos_matrix(self, encoded_pos_matrix, encoded_order_matrix):
        for i in range(10):
            self.UDP_broadcast(bytes(encoded_pos_matrix, "ascii"), "", config.BASE_ELEVATOR_PORT+config.ELEV_ID)
        for i in range(10):
            self.UDP_broadcast(bytes(encoded_order_matrix, "ascii"), "", config.BASE_ELEVATOR_PORT+config.ELEV_ID)
        
        recieved_response = 0
        while recieved_response != config.N_ELEVATORS:
            for i in range(config.N_ELEVATORS): #################mulig problem at den lytter på seg selv
                msg = self.UDP_listen(config.BASE_ELEVATOR_PORT+i)
                if(msg is not int):
                    recieved_response += 1
                    order_matrix = fsm.Fsm.queue.order_json_decode_order_matrix(msg[0])
                    Network.online_elevators[i] = 1
                    #position_matrix = fsm.Fsm.queue.order_json_decode_position_matrix()
                    for j in range(config.N_FLOORS):
                        fsm.Fsm.queue.m_order_matrix[j][i] = order_matrix[j][i]
                else:
                    recieved_response += 1
                    Network.online_elevators[msg-config.BASE_ELEVATOR_PORT] = 0


        





        
        


