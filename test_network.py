import Network
import json
from threading import Thread

    
message = "Hello Petter!"
message_ = {
            "queue info": {
            "queue" : "E3",
            "position" : "E5",
            "message" : message
            }
        }
json_packet = json.dumps(message_)
json_packet = bytes(json_packet, "ascii")
network = Network.Network("localhost", 20009)
#p1 = Thread(target = network.UDP_listen, args=(20009,))
p2 = Thread(target =network.UDP_broadcast, args=(json_packet, '<broadcast>', 20008,))
#p1.start()
p2.start()
while True:
    try:
        p2.join(timeout=3)
        #p1.join(timeout=3)
    except:
        pass
    #network.UDP_broadcast(json_packet, '<broadcast>', 20009)
