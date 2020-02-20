#include "fsm.h"
#include "driver/elevator_hardware.h"


#define UNDEFINED -1
#define IDLE 0
#define RUN 1
#define DOOR_OPEN 2
#define EMERGENCY_STOP 3
#define OBSTRUCTION 4

static int currState = UNDEFINED;
static int nextState = UNDEFINED;

static int prevRegisteredFloor = -1;
static elevator_hardware_motor_direction_t direction;

int fsm_get_current_floor(void){
    return elevator_hardware_get_floor_sensor_signal();
}

int fsm_init(void){
    prevRegisteredFloor = 0;
    direction = DIRN_STOP;
    if (fsm_get_current_floor() == 0){
        elevator_hardware_set_motor_direction(DIRN_STOP);
        elevator_hardware_set_floor_indicator(0);
        nextState = IDLE;
        currState = UNDEFINED;
    }
    else{
        elevator_hardware_set_motor_direction(DIRN_DOWN);
        while(1){
            if (fsm_get_current_floor() == 0){
                elevator_hardware_set_floor_indicator(0);
                elevator_hardware_set_motor_direction(DIRN_STOP);
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
                elevator_hardware_set_motor_direction(DIRN_STOP);
                order_poll();
                if(order_get_top(prevRegisteredFloor).set){
                    nextState = RUN;
                    direction = DIRN_UP;
                } else if (order_get_bottom(prevRegisteredFloor).set){
                    nextState = RUN;
                    direction = DIRN_DOWN;
                }
                break;

            case RUN:

                elevator_hardware_set_motor_direction(direction);
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

                elevator_hardware_set_motor_direction(DIRN_STOP);
                elevator_hardware_set_door_open_lamp(1);
                timer_start();
                while(1){
                    order_poll();
                    if (timer_expire() == 1){
                        printf("door_lamp off\n\r");
                        elevator_hardware_set_door_open_lamp(0);
                        break;
                    }
                }

                if (order_continue(direction, prevRegisteredFloor)){
                    printf("next state run \n\r)");
                    nextState = RUN;
                } else{
                    printf("next state IDLE\n\r");
                    nextState = IDLE;
                }
                
                break;
                
            

        }
    }
}
