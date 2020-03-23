import fsm
import network
from ctypes import *
from ctypes.util import find_library
import config
import order
from threading import Thread
import time

heis = cdll.LoadLibrary("petter/driver.so")
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
        #print(hei)
        #try:
        #json = hei.decode(encoding='ascii')
        elev.queue.order_json_decode_order_matrix(hei[0])
        #print(elev.queue.m_order_matrix[3][0].order_set)
    #elev.fsm_run()

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



run_elevator_1()