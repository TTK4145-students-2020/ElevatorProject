from ctypes import *
from ctypes.util import find_library
import json
import config

heis = cdll.LoadLibrary("petter/driver.so")

BUTTON_COMMAND = 2

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
            order = Order(i,-1, -1)
            m_order_matrix[i].append(order)


    def order_add(self, order):
        if(OrderMatrix.m_order_matrix[order.floor][order.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[order.floor][order.ELEV_ID].order_type != order.order_type):
            order.order_type = config.BUTTON_MULTI
        order.order_set = 1
        OrderMatrix.m_order_matrix[order.floor][order.ELEV_ID] = order
    
    def order_poll_buttons(self):
        order = Order(-1,-1, -1)
        order_received = 0
        for i in range(config.N_FLOORS):
            if(heis.elevator_hardware_get_button_signal(config.BUTTON_COMMAND, i)):
                order_received = 1
                order.floor = i
                order.order_type = config.BUTTON_COMMAND
                #order.order_set = 1
                self.order_add(order)
                heis.elevator_hardware_set_button_lamp(config.BUTTON_COMMAND,i,1)
                return order_received

            if(heis.elevator_hardware_get_button_signal(config.BUTTON_CALL_DOWN, i)):
                order_received = 1
                order.floor = i
                order.order_type = config.BUTTON_CALL_DOWN
                #order.order_set = 1
                self.order_add(order)
                heis.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,i,1)
                return order_received
            
            if(heis.elevator_hardware_get_button_signal(config.BUTTON_CALL_UP, i)):
                order_received = 1
                order.floor = i
                order.order_type = config.BUTTON_CALL_UP
                #order.order_set = 1
                self.order_add(order)
                heis.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,i,1)
                return order_received
        return order_received
    
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



def test_json():
    o = OrderMatrix()
    order = Order(1,1,1)
    o.order_add(order)
    #print(o.m_order_matrix[1][0].order_set)
    json = o.order_json_encode_order_matrix()
    o.order_json_decode_order_matrix(json)
