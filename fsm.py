from ctypes import *
from ctypes.util import find_library
import config
import order
import network
import time



heis = cdll.LoadLibrary("petter/driver.so")

class Fsm:
    queue = order.OrderMatrix()
    order_is_received = 0
    error_timer_start = 0
    prev_position_other_elevator = -1
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
            if(self.m_next_state == config.IDLE or self.m_next_state == config.DOOR_OPEN):
                Fsm.m_position_matrix[config.N_FLOORS][config.ELEV_ID] = 0
            else:
                Fsm.m_position_matrix[config.N_FLOORS][config.ELEV_ID] = self.m_direction
    
    def fsm_check_failure(self, other_elev, online_elevators):
        order_exist = 0            
        
        for i in range(config.N_FLOORS):
            if(Fsm.queue.m_order_matrix[i][other_elev].order_set == 1):
                order_exist = 1

        if(order_exist == 0):
            #print("restart timer 1")
            Fsm.error_timer_start = time.time()

        for i in range(config.N_FLOORS):
            if(Fsm.m_position_matrix[i][other_elev] == 1 and i != Fsm.prev_position_other_elevator):
                #print("restart timer 2")
                Fsm.prev_position_other_elevator = i
                Fsm.error_timer_start = time.time()

        if(time.time()-Fsm.error_timer_start >= 5 and order_exist == 1 and online_elevators[config.ELEV_ID] == 1): #and online_elevators[other_elev] == 1):
            print("should reassing")
            Fsm.queue.order_reassign_order(other_elev)
        #print("time diff: ", time.time()-Fsm.error_timer_start)

    def fsm_network_loss_state(self):
        other_elev = ( config.ELEV_ID + 1 ) % 2

        for i in range(config.N_FLOORS):
            Fsm.queue.m_order_matrix[i][other_elev].order_set = 0

            """if(Fsm.queue.m_order_matrix[i][config.ELEV_ID].order_set == 1):
                if(Fsm.queue.m_order_matrix[i][config.ELEV_ID].order_type == 2 or Fsm.queue.m_order_matrix[i][config.ELEV_ID].order_type == 5 or Fsm.queue.m_order_matrix[i][config.ELEV_ID].order_type == 4 or Fsm.queue.m_order_matrix[i][config.ELEV_ID].order_type == 6):
                    Fsm.queue.m_order_matrix[i][config.ELEV_ID].order_type = config.BUTTON_COMMAND
                else:
                    Fsm.queue.m_order_matrix[i][config.ELEV_ID].order_set = 0
                
            else:
                heis.elevator_hardware_set_button_lamp(config.BUTTON_COMMAND,i,0)

            for j in range(2):
                heis.elevator_hardware_set_button_lamp(j,i,0)
                heis.elevator_hardware_set_button_lamp(j,i,0)"""



                
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

    def fsm_run(self, online_elevators):
        print("=======fsm run=======")
        timer_start = time.time() 
        other_elev = ( config.ELEV_ID + 1 ) % 2
        run_fsm_network_loss = 1

        while(True):
           
            while(self.m_next_state == config.IDLE):  #idle state
                                #####print order matrix
                #Fsm.queue.print_order_matrix(Fsm.queue.m_order_matrix)
                ######
                #print(self.m_direction)
                #self.m_direction = config.DIRN_STOP
                #self.fsm_update_position()
                if(time.time()-timer_start >= 0.7):
                    timer_start = time.time()
                    Fsm.order_is_received = 0

                if(online_elevators[config.ELEV_ID] == 1):
                    run_fsm_network_loss = 1

                if(online_elevators[config.ELEV_ID] == 0 and run_fsm_network_loss == 1):
                    run_fsm_network_loss = 0
                    self.fsm_network_loss_state()


                heis.elevator_hardware_set_motor_direction(config.DIRN_STOP)
                Fsm.order_is_received = Fsm.queue.order_poll_buttons(Fsm.m_position_matrix, online_elevators, Fsm.order_is_received)
                Fsm.queue.order_light_control()
                self.fsm_check_failure(other_elev, online_elevators)

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
                #####print order matrix
                #Fsm.queue.print_order_matrix(Fsm.queue.m_order_matrix)
                #print(self.m_direction)
                if(time.time()-timer_start >= 0.7):
                    timer_start = time.time()
                    Fsm.order_is_received = 0

                if(online_elevators[config.ELEV_ID] == 1):
                    run_fsm_network_loss = 1

                if(online_elevators[config.ELEV_ID] == 0 and run_fsm_network_loss == 1):
                    run_fsm_network_loss = 0
                    self.fsm_network_loss_state()
                
                heis.elevator_hardware_set_motor_direction(self.m_direction)
                Fsm.order_is_received = Fsm.queue.order_poll_buttons(Fsm.m_position_matrix, online_elevators, Fsm.order_is_received)
                Fsm.queue.order_light_control()
                self.fsm_check_failure(other_elev, online_elevators)


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
                #self.m_direction = config.DIRN_STOP'

                self.fsm_update_position()
                heis.elevator_hardware_set_motor_direction(config.DIRN_STOP)
                heis.elevator_hardware_set_door_open_lamp(1)
                heis.timer_start()

                while(True):
                    if(time.time()-timer_start >= 0.7):
                        Fsm.order_is_received = 0
                        timer_start = time.time()
                    
                    if(online_elevators[config.ELEV_ID] == 1):
                        run_fsm_network_loss = 1

                    if(online_elevators[config.ELEV_ID] == 0 and run_fsm_network_loss == 1):
                        run_fsm_network_loss = 0
                        self.fsm_network_loss_state()

                    Fsm.order_is_received = Fsm.queue.order_poll_buttons(Fsm.m_position_matrix, online_elevators, Fsm.order_is_received)
                    Fsm.queue.order_light_control()
                    self.fsm_check_failure(other_elev, online_elevators)
                    Fsm.queue.order_clear_floor(self.m_prev_registered_floor)
                    if(heis.timer_expire() == 1):
                        heis.elevator_hardware_set_door_open_lamp(0)
                        break                
                ################################ test
                
                #print("-------pos matrix-------")
                #print(Fsm.m_position_matrix)

                if(Fsm.queue.order_continue(self.m_direction, self.m_prev_registered_floor)):
                    self.m_next_state = config.RUN
                
                else:
                    self.m_next_state = config.IDLE





