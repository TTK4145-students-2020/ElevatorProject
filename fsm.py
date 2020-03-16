from ctypes import *
from ctypes.util import find_library
import config
import order


heis = cdll.LoadLibrary("petter/driver.so")

class Fsm:
    queue = order.OrderMatrix()

    def __init__(self):
        self.m_next_state = config.UNDEFINED
        self.m_prev_registered_floor = -1
        self.m_direction = config.DIRN_STOP
        self.m_stop_between_floors = 0

    def fsm_get_current_floor(self):
        return heis.elevator_hardware_get_floor_sensor_signal()

    def fsm_init(self):
        print("=======fsm init=======")
        self.m_prev_registered_floor = 0
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
                if(Fsm.queue.order_continue(self.m_direction, self.m_prev_registered_floor)):
                    self.m_next_state = config.RUN
                
                else:
                    self.m_next_state = config.IDLE


def test():
    elev = Fsm()
    heis.elevator_hardware_init()
    elev.fsm_init()
    elev.fsm_run()

test()


