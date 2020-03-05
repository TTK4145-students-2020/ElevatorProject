import Network
import json

network = Network.Network("localhost", "424242")
message = "Hello World!"
json_packet = json.dumps(message)
network.UDP_broadcast(json_packet, "10.22.229.181", "424242")