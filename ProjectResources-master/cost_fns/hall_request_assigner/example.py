import subprocess
import json

input = {
    "hallRequests" : 
        [[False,False],[True,False],[False,False],[False,True]],
    "states" : {
        "one" : {
            "behaviour":"moving",
            "floor":2,
            "direction":"up",
            "cabRequests":[False,False,True,True]
        },
        "two" : {
            "behaviour":"idle",
            "floor":0,
            "direction":"stop",
            "cabRequests":[False,False,False,False]
        }
    }
}

json_packet = json.dumps(input)
json_packet = bytes(json_packet, "ascii")

process = subprocess.run(["./hall_request_assigner", "--input", json_packet], check=True, stdout=subprocess.PIPE, universal_newlines=True)
output = process.stdout

print(output)