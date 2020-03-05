import Network
import json

network = Network.Network("localhost", 20009)

while True:
    
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
    network.UDP_broadcast(json_packet, "", 20009)