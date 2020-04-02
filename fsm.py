from ctypes import *
from ctypes.util import find_library
import config
import order
import network



heis = cdll.LoadLibrary("petter/driver.so")

class Fsm:
    queue = order.OrderMatrix()
    #netw = network.Network(config.ELEV_ID)
    #send_position = False

    #create position matrix
    m_position_matrix = []
    for i in range(config.N_FLOORS + 1):
        m_position_matrix.append([])
        for j in range(config.N_ELEVATORS):
            m_position_matrix[i].append(0)

    def __init__(self):
        self.m_next_state = config.UNDEFINED
        self.m_prev_registered_floor = -1
        self.m_direction = config.DIRN_STOP
        self.m_stop_between_floors = 0

    def fsm_get_current_floor(self):
        return heis.elevator_hardware_get_floor_sensor_signal()

    def fsm_update_position(self):
        pos =  heis.elevator_hardware_get_floor_sensor_signal()
        if(pos != -1):
            for i in range(config.N_FLOORS):
                Fsm.m_position_matrix[i][config.ELEV_ID] = 0
            Fsm.m_position_matrix[pos][config.ELEV_ID] = 1
            Fsm.m_position_matrix[config.N_FLOORS][config.ELEV_ID] = self.m_direction

    def fsm_init(self):
        print("=======fsm init=======")
        self.m_prev_registered_floor = 0
        Fsm.m_position_matrix[0][config.ELEV_ID] = 1
        self.m_direction = config.DIRN_STOP
        Fsm.queue.order_clear_all()
        if (heis.elevator_hardware_get_floor_sensor_signal() == 0):
            heis.elevator_hardware_set_motor_direction(config.DIRN_STOP)
            heis.elevator_hardware_set_floor_indicator(0)
            self.m_next_state = config.IDLE
        
        else:
            heis.elevator_hardware_set_motor_direction(config.DIRN_DOWN)
            while True:
                if(heis.elevator_hardware_get_floor_sensor_signal() == 0):
                    heis.elevator_hardware_set_floor_indicator(0)
                    heis.elevator_hardware_set_motor_direction(config.DIRN_STOP)
                    self.m_next_state = config.IDLE
                    break

    def fsm_run(self):
        print("=======fsm run=======")
        while(True):
           
            while(self.m_next_state == config.IDLE):  #idle state

                heis.elevator_hardware_set_motor_direction(config.DIRN_STOP)
                Fsm.queue.order_poll_buttons()

                if(self.fsm_get_current_floor() == -1 and Fsm.queue.order_is_set(self.m_prev_registered_floor)):
                    self.m_next_state = config.RUN
                    

                    if(self.m_direction == config.DIRN_DOWN and self.m_stop_between_floors != 1):
                        self.m_direction = config.DIRN_UP
                    
                    elif(self.m_direction == config.DIRN_UP and self.m_stop_between_floors != 1):
                        self.m_direction = config.DIRN_DOWN
                    
                    self.m_stop_between_floors = 1
                
                elif(Fsm.queue.order_get_top(self.m_prev_registered_floor).order_set == 1):
                    self.m_next_state = config.RUN
                    self.m_stop_between_floors = 0
                    self.m_direction = config.DIRN_UP
                
                elif(Fsm.queue.order_get_bottom(self.m_prev_registered_floor).order_set == 1):
                    self.m_next_state = config.RUN
                    self.m_stop_between_floors = 0
                    self.m_direction = config.DIRN_DOWN
            

            while(self.m_next_state == config.RUN): #run state
                heis.elevator_hardware_set_motor_direction(self.m_direction)
                Fsm.queue.order_poll_buttons()

                if(self.fsm_get_current_floor() != -1):
                    valid_floor = self.fsm_get_current_floor()
                    self.fsm_update_position()

                    if(valid_floor != -1):
                        self.m_prev_registered_floor = valid_floor
                        heis.elevator_hardware_set_floor_indicator(valid_floor)
                    
                    if(Fsm.queue.order_stop_at_floor(self.m_direction, self.m_prev_registered_floor)):
                        self.m_next_state = config.DOOR_OPEN
                        break
                    
                    if(Fsm.queue.order_get_bottom(self.m_prev_registered_floor).order_set != 1 and Fsm.queue.order_get_top(self.m_prev_registered_floor).order_set != 1):
                        self.m_next_state = config.IDLE

            while(self.m_next_state == config.DOOR_OPEN): #door open state
                heis.elevator_hardware_set_motor_direction(config.DIRN_STOP)
                heis.elevator_hardware_set_door_open_lamp(1)
                heis.timer_start()


                while(True):
                    Fsm.queue.order_poll_buttons()
                    Fsm.queue.order_clear_floor(self.m_prev_registered_floor)
                    if(heis.timer_expire() == 1):
                        heis.elevator_hardware_set_door_open_lamp(0)
                        break                
                ################################ test
                Fsm.queue.print_order_matrix(Fsm.queue.m_order_matrix)
                print("-------pos matrix-------")
                print(Fsm.m_position_matrix)

                if(Fsm.queue.order_continue(self.m_direction, self.m_prev_registered_floor)):
                    self.m_next_state = config.RUN
                
                else:
                    self.m_next_state = config.IDLE





