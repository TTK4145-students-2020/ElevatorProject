#include "fsm.h"

static int m_nextState = UNDEFINED;

static int m_prevRegisteredFloor = -1;

static elevator_hardware_motor_direction_t m_direction;

static int m_stopBetweenFloors = 0;

int fsm_get_current_floor(void){

    return hardware_read_all_floor_sensors();
}



int fsm_init(void){

    m_prevRegisteredFloor = 0;
    m_direction = DIRN_STOP;
    order_clear_all();

    if (hardware_read_floor_sensor(0)){
        hardware_command_movement(DIRN_STOP);
        hardware_command_floor_indicator_on(0);
        m_nextState = IDLE;
    }
    else{
        hardware_command_movement(DIRN_DOWN);

        while(1){

            if (hardware_read_floor_sensor(0)){
                hardware_command_floor_indicator_on(0);
                hardware_command_movement(DIRN_STOP);
                m_nextState = IDLE;
                return 0;
            }               

        }
    }
    return 0;
}

int fsm_run(void){

    while(1){

        switch(m_nextState){

            case IDLE:

                if (hardware_read_stop_signal()){
                    m_nextState = EMERGENCY_STOP;
                    break;
                }
                
                hardware_command_movement(DIRN_STOP);
                order_poll_buttons();

                if(fsm_get_current_floor() == -1 && order_is_set(m_prevRegisteredFloor)){
                    
                    m_nextState = RUN;

                    if(m_direction == DIRN_DOWN && !m_stopBetweenFloors){
                        m_direction = DIRN_UP;

                    } else if(m_direction == DIRN_UP && !m_stopBetweenFloors){
                        m_direction = DIRN_DOWN;
                    }
                    m_stopBetweenFloors = 1;

                } else if(order_get_top(m_prevRegisteredFloor).set){
                    m_nextState = RUN;
                    m_stopBetweenFloors = 0;
                    m_direction = DIRN_UP;

                } else if (order_get_bottom(m_prevRegisteredFloor).set){
                    m_nextState = RUN;
                    m_stopBetweenFloors = 0;
                    m_direction = DIRN_DOWN;
                }
                break;
              

            case RUN:

                if (hardware_read_stop_signal()){
                    m_nextState = EMERGENCY_STOP;
                    break;
                }

                hardware_command_movement(m_direction);
                order_poll_buttons();
                
                if(fsm_get_current_floor() != -1){
                    int validFloor = fsm_get_current_floor();

                    if (validFloor != -1){
                        m_prevRegisteredFloor = validFloor;
                        hardware_command_floor_indicator_on(validFloor);
                    }
                                       
                    if(order_stop_at_floor(m_direction, m_prevRegisteredFloor)){
                        m_nextState = DOOR_OPEN;
                        break;
                    }

                    if(!order_get_bottom(m_prevRegisteredFloor).set && !order_get_top(m_prevRegisteredFloor).set){
                        m_nextState = IDLE;
                    }
                }
                break;


            case DOOR_OPEN:
        
                hardware_command_movement(DIRN_STOP);
                hardware_command_door_open(1);
                timer_start();

                while(1){

                    if (hardware_read_stop_signal()){
                        m_nextState = EMERGENCY_STOP;
                        break;
                    }

                    order_poll_buttons();
                    order_clear_floor(m_prevRegisteredFloor);

                    if(hardware_read_obstruction_signal() == 1){
                        timer_start();
                    }

                    if (timer_expire() == 1){
                        hardware_command_door_open(0);
                        break;
                    }
                }

                if (order_continue(m_direction, m_prevRegisteredFloor)){
                    m_nextState = RUN;

                } else{
                    m_nextState = IDLE;
                }
                break;


            case EMERGENCY_STOP:
                hardware_command_movement(DIRN_STOP);
                hardware_command_stop_light(1);
                order_clear_all();
                

                if(fsm_get_current_floor() != -1){
                    hardware_command_door_open(1);
                    m_nextState = DOOR_OPEN;

                }else{
                    m_nextState = IDLE;
                }

                while(hardware_read_stop_signal());

                hardware_command_stop_light(0);
                break;
                
        }
    }
}