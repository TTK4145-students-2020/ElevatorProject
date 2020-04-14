from ctypes import *
from ctypes.util import find_library
import json
import config
import subprocess

heis = cdll.LoadLibrary("petter/driver.so")



class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class Order:

    def __init__(self, floor, order_type, order_set):
        self.floor = floor
        self.order_type = order_type
        self.order_set = order_set
        self.ELEV_ID = config.ELEV_ID
    

class OrderMatrix():
    #create order matrix and position matrix
    m_order_matrix = []
    
    for i in range(config.N_FLOORS):
        m_order_matrix.append([])
        for j in range(config.N_ELEVATORS):
            order = Order(i,0, 0)
            m_order_matrix[i].append(order)

    def order_add(self, order, pos_matrix):
        if(order.order_type == config.BUTTON_COMMAND):
            if(OrderMatrix.m_order_matrix[order.floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[order.floor][config.ELEV_ID].order_type != order.order_type):
                order.order_type = config.BUTTON_MULTI
            order.order_set = 1
            OrderMatrix.m_order_matrix[order.floor][config.ELEV_ID] = order

        else:
            elev_id = self.order_designate_elevator(pos_matrix, order)
            #print("elev_id:", elev_id)
            if(OrderMatrix.m_order_matrix[order.floor][elev_id].order_set == 1 and OrderMatrix.m_order_matrix[order.floor][elev_id].order_type != order.order_type):
                order.order_type = config.BUTTON_MULTI
            order.order_set = 1
            OrderMatrix.m_order_matrix[order.floor][elev_id] = order
    
    def order_poll_buttons(self, pos_matrix, online_elevators):
        #print(sum(online_elevators))

        order = Order(-1,-1, -1)
        order_is_received = 0
        for i in range(config.N_FLOORS):
            if(heis.elevator_hardware_get_button_signal(config.BUTTON_COMMAND, i)):
                order_is_received = 1
                order.floor = i
                order.order_type = config.BUTTON_COMMAND
                #order.order_set = 1
                self.order_add(order, pos_matrix)
                heis.elevator_hardware_set_button_lamp(config.BUTTON_COMMAND,i,1)
                return order_is_received

            if(heis.elevator_hardware_get_button_signal(config.BUTTON_CALL_DOWN, i)):
                if(sum(online_elevators) <= 1):
                    return    
                order_is_received = 1
                order.floor = i
                order.order_type = config.BUTTON_CALL_DOWN
                #order.order_set = 1
                self.order_add(order, pos_matrix)
                heis.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,i,1)
                return order_is_received
            if(heis.elevator_hardware_get_button_signal(config.BUTTON_CALL_UP, i)):
                if(sum(online_elevators) <= 1):
                    return    
                order_is_received = 1
                order.floor = i
                order.order_type = config.BUTTON_CALL_UP
                #order.order_set = 1
                self.order_add(order, pos_matrix)
                heis.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,i,1)
                return order_is_received
        return order_is_received
    
    def order_designate_elevator(self, pos_matrix, order):
        cab_req_elev_0 = [False, False, False, False]
        cab_req_elev_1 = [False, False, False, False]
        hall_req = [[False,False],[False,False],[False,False],[False,False]]
        position_elev_0 = 0
        position_elev_1 = 0
        direction_elev_0 = "stop"
        direction_elev_1 = "stop"
        behaviour_elev_0 = "moving"
        behaviour_elev_1 = "moving"



        #print("order floor:", order.floor, "order type:", order.order_type)
        if(order.order_type == config.BUTTON_CALL_UP):
      
            hall_req[order.floor][0] = True
        
        elif(order.order_type == config.BUTTON_CALL_DOWN):
  
            hall_req[order.floor][1] = True

        #print("hallreq", hall_req)
        for i in range(config.N_FLOORS):
            if(pos_matrix[i][0] == 1):
                position_elev_0 = i
            if(pos_matrix[i][1] == 1):
                position_elev_1 = i

            if(OrderMatrix.m_order_matrix[i][0].order_set == 1 and (OrderMatrix.m_order_matrix[i][0].order_type == config.BUTTON_COMMAND or OrderMatrix.m_order_matrix[i][0].order_type == config.BUTTON_MULTI)):
                cab_req_elev_0[i] = True
            if(OrderMatrix.m_order_matrix[i][1].order_set == 1 and (OrderMatrix.m_order_matrix[i][1].order_type == config.BUTTON_COMMAND or OrderMatrix.m_order_matrix[i][1].order_type == config.BUTTON_MULTI)):
                cab_req_elev_1[i] = True


        if(pos_matrix[config.N_FLOORS][0] == -1):
            direction_elev_0 = "down"
        elif(pos_matrix[config.N_FLOORS][0] == 1):
            direction_elev_0 = "up"
        else:
            direction_elev_0 = "stop"
        
        if(pos_matrix[config.N_FLOORS][1] == -1):
            direction_elev_1 = "down"
        elif(pos_matrix[config.N_FLOORS][1] == 1):
            direction_elev_1 = "stop"
        else:
            direction_elev_1 = "stop"





        input = {
            "hallRequests" : hall_req,
            "states" : {
                "zero" : {
                    "behaviour" : behaviour_elev_0,
                    "floor" : position_elev_0,
                    "direction" : direction_elev_0,
                    "cabRequests" : cab_req_elev_0
                },
                "one" : {
                    "behaviour": behaviour_elev_1,
                    "floor" : position_elev_1,
                    "direction" : direction_elev_1,
                    "cabRequests" : cab_req_elev_1  
                }
            }
        }
        json_packet = json.dumps(input)
        #print("input:", input)
        json_packet = bytes(json_packet, "ascii")
        process = subprocess.run(["./ProjectResources-master/cost_fns/hall_request_assigner/hall_request_assigner", "--input", json_packet], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = process.stdout
        output = json.loads(output)
        #print("one:", output["one"])
        #print("zero:", output["zero"])
        
        for i in range(config.N_FLOORS):
            for j in range(2):
                if(output["zero"][i][j] == True):
                    return 0
                if(output["one"][i][j] == True):
                    return 1



    def order_clear_floor(self, floor):
        #for i in range(config.N_BUTTONS):
        OrderMatrix.m_order_matrix[floor][config.ELEV_ID].order_set = 0
        for i in range(config.N_BUTTONS):
            heis.elevator_hardware_set_button_lamp(i,floor,0)
        
    def order_clear_all(self):
        for i in range(config.N_FLOORS):
            for j in range(config.N_BUTTONS):
                OrderMatrix.m_order_matrix[i][config.ELEV_ID].order_set = 0
                heis.elevator_hardware_set_button_lamp(j,i,0)
        
    def order_is_set(self, floor):
        for i in range(config.N_ELEVATORS):
            if(OrderMatrix.m_order_matrix[floor][i].order_set == 1):
                return 1
        return 0

    def order_json_encode_order_matrix(self):
        json_packet = json.dumps(OrderMatrix.m_order_matrix, cls=MyEncoder)
        return json_packet

    def order_json_decode_order_matrix(self, json_packet):
        json_packet = json.JSONDecoder().decode(json_packet)
        order_matrix = []
        for i in range(config.N_FLOORS):
            order_matrix.append([])
            for j in range(config.N_ELEVATORS):
                floor = json_packet[i][j]["floor"]
                order_type = json_packet[i][j]["order_type"]
                order_set = json_packet[i][j]["order_set"]
                order = Order(floor,order_type, order_set)
                order_matrix[i].append(order)
            #OrderMatrix.m_order_matrix[i] = order_matrix
        return order_matrix
    
    def order_json_encode_position_matrix(self, pos_matrix):
        return json.dumps(pos_matrix)

    def order_json_decode_position_matrix(self, json_pos_matrix):
        json_packet = json.JSONDecoder().decode(json_pos_matrix)
        m_position_matrix = []
        for i in range(config.N_FLOORS + 1):
            m_position_matrix.append([])
            for j in range(config.N_ELEVATORS):
                m_position_matrix[i].append(json_packet[i][j])

        return m_position_matrix
            

    def order_get_top(self, floor):
        order = OrderMatrix.m_order_matrix[config.N_FLOORS-1][config.ELEV_ID]

        for i in range(floor, config.N_FLOORS):
            for j in range(config.N_BUTTONS):
                if(OrderMatrix.m_order_matrix[i][config.ELEV_ID].order_set == 1):
                    order = OrderMatrix.m_order_matrix[i][config.ELEV_ID]
        return order
    
    def order_get_bottom(self, floor):
        order = OrderMatrix.m_order_matrix[0][config.ELEV_ID]

        for i in range(floor,-1,-1):
            for j in range(config.N_BUTTONS):
                if(OrderMatrix.m_order_matrix[i][config.ELEV_ID].order_set == 1):
                    order = OrderMatrix.m_order_matrix[i][config.ELEV_ID]
        return order

    def order_stop_at_floor(self, direction, current_floor):
        
        if(direction == config.DIRN_DOWN):
            if(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and (OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_CALL_DOWN or OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_MULTI)):
                return 1
            elif(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_COMMAND):
                return 1
            elif(self.order_get_bottom(current_floor).floor == current_floor and self.order_get_bottom(current_floor).order_set == 1):
                return 1
            elif( current_floor == 0):
                return 1
        
        elif(direction == config.DIRN_UP):
            
            if(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and (OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_CALL_UP or OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_MULTI)):
                return 1
            elif(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == (config.BUTTON_COMMAND or config.BUTTON_MULTI)):
                return 1
            elif(self.order_get_top(current_floor).floor == current_floor and self.order_get_top(current_floor).order_set == 1):
                return 1
            elif(current_floor == config.N_FLOORS-1):
                return 1
        
        return 0

    def order_continue(self, direction, current_floor):
        if(direction == config.DIRN_DOWN):
            if(self.order_get_bottom(current_floor).order_set == 1 and self.order_get_bottom(current_floor).floor < current_floor):
                return 1
        
        elif(direction == config.DIRN_UP):
            if(self.order_get_top(current_floor).order_set == 1 and self.order_get_top(current_floor).floor > current_floor):
                return 1

    def order_reassign_order(self, id):
        other_elev = ( id + 1 ) % 2
        for i in range(config.N_FLOORS):
            if(OrderMatrix.m_order_matrix[i][id].order_set == 1 and OrderMatrix.m_order_matrix[i][id].order_type != config.BUTTON_COMMAND):
                OrderMatrix.m_order_matrix[i][other_elev].order_set = OrderMatrix.m_order_matrix[i][id].order_set
                OrderMatrix.m_order_matrix[i][other_elev].order_type = OrderMatrix.m_order_matrix[i][id].order_type
                OrderMatrix.m_order_matrix[i][id].order_set = 0

        """temp_order = []
        for i in range(config.N_FLOORS):
            temp_order.append(OrderMatrix.m_order_matrix[i][id])
        OrderMatrix.m_order_matrix[:][id] = 0
        other_elev = ( id + 1 ) % 2
        #print(other_elev)
        
        for i in range(config.N_FLOORS):
            order = temp_order[i]
            if(order.order_type == config.BUTTON_COMMAND):
                OrderMatrix.m_order_matrix[order.floor][other_elev] = 0

            else:
                elev_id = other_elev
                if(OrderMatrix.m_order_matrix[order.floor][other_elev].order_set == 1 and OrderMatrix.m_order_matrix[order.floor][other_elev].order_type != order.order_type):
                    order.order_type = config.BUTTON_MULTI
                order.order_set = 1
                OrderMatrix.m_order_matrix[order.floor][other_elev] = order"""
        



    ###### skal fjernes, bare for at det skal være lett å se ordre matrisen
    def print_order_matrix(self, order_matrix):
        print("--------order matrix------")
        for i in range(config.N_FLOORS):
            print(order_matrix[i][0].order_set, "\t", order_matrix[i][1].order_set)



def test_json():
    o = OrderMatrix()
    o.m_order_matrix[0][0].order_set = 1
    o.m_order_matrix[0][0].order_type = 2
    o.print_order_matrix(o.m_order_matrix)
    o.order_reassign_order(0)
    o.print_order_matrix(o.m_order_matrix)
    print("sssss")
    print(o.m_order_matrix[0][1].order_type)

test_json()