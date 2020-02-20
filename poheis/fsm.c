#include "fsm.h"


#define UNDEFINED -1
#define IDLE 0
#define RUN 1
#define DOOR_OPEN 2
#define EMERGENCY_STOP 3
#define OBSTRUCTION 4

static int currState = UNDEFINED;
static int nextState = UNDEFINED;

static int prevRegisteredFloor = -1;
static int direction;

int fsm_get_current_floor(void){
    return hardware_read_all_floor_sensors();
}

// int fsm_emergency_poll(void){
//     if (hardware_read_stop_signal()){
//         currState = nextState;
//         nextState = EMERGENCY_STOP;
//     }
//     return 0;
// }

// int fsm_move_towards_current_order(order_t order){
//     if(order.floor > prevRegisteredFloor){
//         direction = HARDWARE_MOVEMENT_UP;
//     } else if (order.floor < prevRegisteredFloor){
//         direction = HARDWARE_MOVEMENT_DOWN;
//     }
//     hardware_command_movement(direction);
//     return 0;
// }


int fsm_init(void){
    prevRegisteredFloor = 0;
    direction = 0;
    if (hardware_read_floor_sensor(0)){
        hardware_command_movement(0);
        hardware_command_floor_indicator_on(0);
        nextState = IDLE;
        currState = UNDEFINED;
    }
    else{
        hardware_command_movement(HARDWARE_MOVEMENT_DOWN);
        while(1){
            if (hardware_read_floor_sensor(0)){
                hardware_command_floor_indicator_on(0);
                hardware_command_movement(HARDWARE_MOVEMENT_STOP);
                nextState = IDLE;
                currState = UNDEFINED;
                return 0;
            }               

        }
    }
    return 0;
}

int fsm_run(void){
    while(1){
        switch(nextState){
            case IDLE:
                if (hardware_read_stop_signal()){
                    nextState = EMERGENCY_STOP;
                    break;
                }

                hardware_command_movement(HARDWARE_MOVEMENT_STOP);
                order_poll();
                if(order_get_top(prevRegisteredFloor).set){
                    nextState = RUN;
                    direction = HARDWARE_MOVEMENT_UP;
                } else if (order_get_bottom(prevRegisteredFloor).set){
                    nextState = RUN;
                    direction = HARDWARE_MOVEMENT_DOWN;
                }
                break;

            case RUN:
                if (hardware_read_stop_signal()){
                    nextState = EMERGENCY_STOP;
                    break;
                }
                hardware_command_movement(direction);
                order_poll();
                
                if(fsm_get_current_floor() != -1){
                    prevRegisteredFloor = fsm_get_current_floor();
                    if(order_stop_at_floor(direction, prevRegisteredFloor)){
                        order_clear_floor(prevRegisteredFloor);
                        nextState = DOOR_OPEN;
                        break;
                    }
                    if(!order_get_bottom(prevRegisteredFloor).set && !order_get_top(prevRegisteredFloor).set){
                        nextState = IDLE;
                    }
                }
                
                
               
                break;

            case DOOR_OPEN:
                if (hardware_read_stop_signal()){
                    nextState = EMERGENCY_STOP;
                    break;
                }

                hardware_command_movement(HARDWARE_MOVEMENT_STOP);
                hardware_command_door_open(1);
                timer_start();

                while(1){
                    order_poll();
                    if(hardware_read_obstruction_signal() == 1){
                        timer_start();
                    }
                    if (timer_expire() == 1){
                        hardware_command_door_open(0);
                        break;
                    }
                }

                if (order_continue(direction, prevRegisteredFloor)){
                    nextState = RUN;
                } else{
                    nextState = IDLE;
                }
                
                break;
            case EMERGENCY_STOP:
                hardware_command_movement(HARDWARE_MOVEMENT_STOP);
                order_clear_all();

                if(fsm_get_current_floor() != -1){
                    hardware_command_door_open(1);
                    nextState = DOOR_OPEN;
                }else{
                    nextState = IDLE;
                }
                while(hardware_read_stop_signal());
                break;
                
                
               
                
                
                
            

        }
    }
}
