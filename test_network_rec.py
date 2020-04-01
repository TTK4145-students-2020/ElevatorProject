import network
import json
from threading import Thread
import order
import time
import fsm
from ctypes import *
from ctypes.util import find_library
import config
import order

heis = cdll.LoadLibrary("petter/driver.so")

o = order.OrderMatrix()
order = order.Order(1,1,1)
o.order_add(order)
#print(o.m_order_matrix[1][0].order_set)
json = o.order_json_encode_order_matrix()
json = bytes(json, "ascii")
netw = network.Network(ID = 0)
#json = json.decode(encoding='ascii')
elev = fsm.Fsm()
json = bytes(elev.queue.order_json_encode_position_matrix(elev.m_position_matrix), "ascii")
melding = bytes("alive", "ascii")


def network_test():
    #netw = network.Network(1)'
    while True:
        for i in range(10):
            netw.UDP_broadcast(bytes("alive", "ascii"), "", 20000)

        msg = netw.UDP_listen(20001)
        print(msg)


def send(json):
    while True:
        print("printer")
        #time.sleep(1)
        netw.UDP_broadcast(json, "", 20000)

def recv():
    
    while True:
        hei = netw.UDP_listen(20000)
        print(hei[0])
        #o.order_json_decode_order_matrix(hei[0])
        #print(o.m_order_matrix)
        #print(elev.queue.order_json_decode_position_matrix(hei[0]))
    #except:
        #print("couldnt fix order matrix")


def thread_test_send():
    elev = fsm.Fsm()
    heis.elevator_hardware_init()
    elev.fsm_init()
    p1 = Thread(target= elev.fsm_run)
    p2 = Thread(target =send, args=(melding,)) #network.UDP_broadcast, args=(json, '', 20000))
    #p1 = Thread(target = network.UDP_listen, args=(20000,))
    p3 = Thread(target= recv)
    p1.start()
    p2.start()
    p3.start()
    #p2.join()

def thread_test_rcv():        
    p1 = Thread(target= recv)
    p1.start()

thread_test_send()