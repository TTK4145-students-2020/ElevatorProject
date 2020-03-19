import Network
import json
from threading import Thread
import order

o = order.OrderMatrix()
order = order.Order(1,1,1)
o.order_add(order)
#print(o.m_order_matrix[1][0].order_set)
json = o.order_json_encode_order_matrix()
json = bytes(json, "ascii")
network = Network.Network(ID = 0)



def send(json):
    
    while True:
        network.UDP_broadcast(json, "<broadcast>", 20008)

def recv():
    #network = Network.Network(ID = 1)
    while True:
        network.UDP_listen(20008)


recv()