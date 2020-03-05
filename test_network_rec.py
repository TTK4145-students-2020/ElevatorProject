# import Network
# import json
# from threading import Thread

# network = Network.Network("localhost", 20009)
# message = "Hello Emre!"
# message_ = {
#             "queue info": {
#             "queue" : "E3",
#             "position" : "E5",
#             "message" : message
#             }
#         }
# json_packet = json.dumps(message_)
# json_packet = bytes(json_packet, "ascii")
# p1 = Thread(network.UDP_listen, target=(20009,))
# p2 = Thread(network.UDP_broadcast, target=(json_packet, '<broadcast>', 20008))
# p1.start()
# p2.start()
# while True:
#     p1.join(timeout=3)
#     p2.join(timeout=3)
#     # msg = network.UDP_listen(20009)
#     # print(msg)

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
network = Network.Network("localhost", 20008)
p1 = Thread(target = network.UDP_listen, args=(20008,))
p2 = Thread(target =network.UDP_broadcast, args=(json_packet, '<broadcast>', 20009,))
p1.start()
p2.start()
while True:
    try:
        p1.join(timeout=3)
    except:
        pass
    p2.join(timeout=3)
    #network.UDP_broadcast(json_packet, '<broadcast>', 20009)
