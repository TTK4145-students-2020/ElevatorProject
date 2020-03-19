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
#json = json.decode(encoding='ascii')



def send(json):
    while True:
        network.UDP_broadcast(json, "", 20008)

def recv():
    hei, address = network.UDP_listen(20008)
    #print(hei)
    #try:
    json = hei.decode(encoding='ascii')
    o.order_json_decode_order_matrix(json)
    #print(o.m_order_matrix)
    #except:
        #print("couldnt fix order matrix")


def test():
    o.order_json_decode_order_matrix(json)
    print(o.m_order_matrix)


recv()