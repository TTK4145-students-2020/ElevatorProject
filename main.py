import fsm
import network
from ctypes import *
from ctypes.util import find_library
import config
import order
from threading import Thread
import time

heis = cdll.LoadLibrary("petter/driver.so")



def main():
    netw = network.Network(config.ELEV_ID)
    elev = fsm.Fsm()
    heis.elevator_hardware_init()
    elev.fsm_init()
    p1 = Thread(target= elev.fsm_run)
    p2 = Thread(target= netw.msg_receive_handler, args=(elev,))
    p3 = Thread(target= netw.msg_send_handler, args=(elev,))
    
    p1.start()
    p2.start()
    p3.start()

            
                

################### tester og dritt
"""    while True: #################dette virker ikke
        #print(1)
        #print(netw.online_elevators)
        #print(elev.queue.order_poll_buttons())
        if(elev.queue.order_poll_buttons()):
            print("update order queue")
            netw.update_order_matrix(elev.queue.order_json_encode_order_matrix())
        #print(elev.fsm_get_current_floor() != -1)
        #print(elev.m_prev_registered_floor != elev.fsm_get_current_floor())
        #print(elev.m_prev_registered_floor)
        if(elev.fsm_get_current_floor() != -1 and elev.m_prev_registered_floor != elev.fsm_get_current_floor()):
            print("update floor")
            netw.update_pos_matrix(elev.queue.order_json_encode_position_matrix(elev.m_position_matrix))

        for i in range(config.N_ELEVATORS):
            if(i != config.ELEV_ID):
                msg = netw.UDP_listen(config.BASE_ELEVATOR_PORT+i)
                print(msg)
                if(isinstance(msg, int) == 0):
                    netw.online_elevators[i] = 1
                    try:
                        elev.queue.order_json_decode_position_matrix(msg[0])
                    except:
                        pass
                    try:
                        elev.queue.order_json_decode_order_matrix(msg[0])
                    except:
                        pass
                    netw.UDP_broadcast(bytes("alive", "ascii"), "", config.BASE_ELEVATOR_PORT+config.ELEV_ID)
                else:
                    netw.online_elevators[i] = 0"""

def update_elevator_online_status(port):
    while True:
        hei = netw.UDP_listen(port)
        if(hei is not int):
            elev.queue.order_json_decode_order_matrix(hei[0])
            netw.online_elevators[port-config.BASE_ELEVATOR_PORT] = 1

            while True: #send confirmation message
                netw.UDP_broadcast(bytes(elev.queue.order_json_encode_order_matrix(), "ascii"),"", 20000)

        else:
            netw.online_elevators[hei-config.BASE_ELEVATOR_PORT] = 0

        if(netw.online_elevators[port-config.BASE_ELEVATOR_PORT] == 0):
            while True:
                netw = network.Network(port-config.BASE_ELEVATOR_PORT)
                #heinetw.UDP_listen()



netw = network.Network(0)

def run_elevator_1():
    elev = fsm.Fsm()
    heis.elevator_hardware_init()
    elev.fsm_init()
    p1 = Thread(target= elev.fsm_run)
    #p2 = Thread(target= netw.UDP_listen, args=(20000,))
    
    p1.start()
    while True:
        hei = netw.UDP_listen(20000)
        if(hei is not int):
            elev.queue.order_json_decode_order_matrix(hei[0])
            #sende ut confirmation melding
        else:
            #netw.online_elevators[hei-20000] = 0
  
            print(netw.online_elevators)


def run_elevator_2():
    
    elev = fsm.Fsm()
    heis.elevator_hardware_init()
    elev.fsm_init()
    #netw = network.Network(1)
    p1 = Thread(target= elev.fsm_run)
    
    #p2 = Thread(target= netw.UDP_broadcast, args=(bytes(elev.queue.order_json_encode_order_matrix(), "ascii"), "", 20000,))
    p1.start()
    while True:
        netw.UDP_broadcast(bytes(elev.queue.order_json_encode_order_matrix(), "ascii"),"", 20000)
    #elev.queue.order_json_encode_order_matrix()
        #print(p2.is_alive())

def test():
    #elev = fsm.Fsm()
    #heis.elevator_hardware_init()
    #elev.fsm_init()
    #p1 = Thread(target= elev.fsm_run)
    #p2 = Thread(target= netw.UDP_listen, args=(20000,))
    #p1.start()
    #ord = order.Order(1,1,1)
    #elev.queue.order_add(ord)

    o = order.OrderMatrix()
    while True:
        hei = netw.UDP_listen(20000)
        #print(hei)
        #try:
        #json = hei.decode(encoding='ascii')
        o.order_json_decode_order_matrix(hei[0])
        print(o.m_order_matrix[0][0].order_set)


main()