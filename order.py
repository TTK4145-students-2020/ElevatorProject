from ctypes import *
from ctypes.util import find_library
import config

heis = cdll.LoadLibrary("petter/driver.so")

BUTTON_COMMAND = 2

class Order:

    def __init__(self, floor, order_type, order_set):
        self.floor = floor
        self.order_type = order_type
        self.order_set = order_set
        self.ELEV_ID = config.ELEV_ID
    

class OrderMatrix():
    #create order matrix
    m_order_matrix = []
    for i in range(config.N_FLOORS):
        m_order_matrix.append([])
        for j in range(config.N_ELEVATORS):
            order = Order(i,-1, -1)
            m_order_matrix[i].append(order)

    def order_add(self, order):
        order.order_set = 1
        OrderMatrix.m_order_matrix[order.floor][order.ELEV_ID] = order
    
    def order_poll_buttons(self):
        order = Order(-1,-1, -1)
        for i in range(config.N_FLOORS):
            if(heis.elevator_hardware_get_button_signal(config.BUTTON_COMMAND, i)):
                order.floor = i
                order.order_type = config.BUTTON_COMMAND
                order.order_set = 1
                self.order_add(order)
                heis.elevator_hardware_set_button_lamp(config.BUTTON_COMMAND,i,1)

            if(heis.elevator_hardware_get_button_signal(config.BUTTON_CALL_DOWN, i)):
                order.floor = i
                order.order_type = config.BUTTON_CALL_DOWN
                order.order_set = 1
                self.order_add(order)
                heis.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,i,1)
            
            if(heis.elevator_hardware_get_button_signal(config.BUTTON_CALL_UP, i)):
                order.floor = i
                order.order_type = config.BUTTON_CALL_UP
                order.order_set = 1
                self.order_add(order)
                heis.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,i,1)
    
    def order_clear_floor(self, floor):
        for i in range(config.N_BUTTONS):
            OrderMatrix.m_order_matrix[floor][config.ELEV_ID].order_set = 0
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
            if(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_CALL_DOWN):
                return 1
            elif(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_COMMAND):
                return 1
            elif(self.order_get_bottom(current_floor).floor == current_floor and self.order_get_bottom(current_floor).order_set == 1):
                return 1
            elif( current_floor == 0):
                return 1
        
        elif(direction == config.DIRN_UP):
            if(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_CALL_UP):
                return 1
            elif(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_COMMAND):
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


    


def test():
    l = Order(3,1,1)
    h = OrderMatrix()
    #print(h.m_order_matrix[0][0].order_set)
    #h.order_add(l)
    #print(h.order_get_top(0).floor)
    #print(h.m_order_matrix[0][0].floor)
    #l.m_order_matrix[0][0] = 1
    #print(h.m_order_matrix)
    #l.order_get_order_matrix(1,1)
    #h.order_poll_buttons()

#print(test())