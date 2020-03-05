import Network
import json

network = Network.Network("localhost", 20009)

while True:
    
    msg = network.UDP_listen(20009)
    print(msg)