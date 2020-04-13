import subprocess
import json

input = {
    "hallRequests" : 
        [[False,False],[False,False],[False,False],[False,False]],
    "states" : {
        "zero" : {
            "behaviour":"moving",
            "floor":2,
            "direction":"up",
            "cabRequests":[False,False,False,True]
        },
        "one" : {
            "behaviour":"idle",
            "floor":0,
            "direction":"stop",
            "cabRequests":[False,False,False,False]
        }
    }
}

json_packet = json.dumps(input)
json_packet = bytes(json_packet, "ascii")

process = subprocess.run(["./cost_fns/hall_request_assigner/hall_request_assigner", "--input", json_packet], check=True, stdout=subprocess.PIPE, universal_newlines=True)
output = process.stdout
output = json.loads(output)
#print(output["one"][1][1])
print(output)