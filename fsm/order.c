#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "driver/elevator_hardware.h"
#include "order.h"

int order_add(order_t order){
    order.set = true;
    orderQueue[order.floor][order.orderType] = order;
    return 0;
}

int order_poll(void){
    order_t order;
    for(int i = 0; i < N_FLOORS; i++){
        if(elevator_hardware_get_button_signal(BUTTON_COMMAND, i)){
            //printf("%d\n\r", i);
            order.floor = i;
            order.orderType = BUTTON_COMMAND;
            order.set = 1;
            order_add(order);
            elevator_hardware_set_button_lamp(BUTTON_COMMAND, i, 1);
        }
        if(elevator_hardware_get_button_signal(BUTTON_CALL_DOWN, i)){
            order.floor = i;
            order.orderType = BUTTON_CALL_DOWN;
            order.set = 1;
            order_add(order);
            elevator_hardware_set_button_lamp(BUTTON_CALL_DOWN, i, 1);
        }
        if(elevator_hardware_get_button_signal(BUTTON_CALL_UP, i)){
            order.floor = i;
            order.orderType = BUTTON_CALL_UP;
            order.set = 1;
            order_add(order);
            elevator_hardware_set_button_lamp(BUTTON_CALL_UP, i, 1);

        }
    }
    return 0;
}

int order_clear_floor(int floor){
    for (int j = 0; j < orderTypes; j++){
        if (orderQueue[floor][j].floor == floor){
            orderQueue[floor][j].set = 0;
        }   
    }
    return 0;
}

void order_clear_all(void){
    for (int i = 0; i < FLOORS; i++){
        for (int j = 0; j < orderTypes; j++){
                orderQueue[i][j].set = 0;
        }
    }
}

order_t order_get(int floor, int orderType){
    return orderQueue[floor][orderType];
}

order_t order_get_top(int floor){

    order_t o = orderQueue[FLOORS][orderTypes];

    for(int i = floor; i < FLOORS; i++){
        for (int j = 0; j < orderTypes; j++){
            if(orderQueue[i][j].set == true){
                o = orderQueue[i][j];
            }
        }
    }
    return o;
}

order_t order_get_bottom(int floor){

    order_t o = orderQueue[0][orderTypes];

    for(int i = floor; i > -1; i--){
        for (int j = 0; j < orderTypes; j++){
            if(orderQueue[i][j].set == true){
                o = orderQueue[i][j];
            }
        }
    }
    return o;
}



int order_stop_at_floor(elevator_hardware_motor_direction_t direction, int Currfloor){
    switch(direction){
        case DIRN_DOWN:
            return orderQueue[Currfloor][BUTTON_CALL_DOWN].set || orderQueue[Currfloor][BUTTON_COMMAND].set || ((order_get_bottom(Currfloor).floor == Currfloor) && order_get_bottom(Currfloor).set) || Currfloor == 0;
        case DIRN_UP:
            return orderQueue[Currfloor][BUTTON_CALL_UP].set || orderQueue[Currfloor][BUTTON_COMMAND].set || ((order_get_top(Currfloor).floor == Currfloor) && order_get_top(Currfloor).set) || Currfloor == N_FLOORS-1;

        default:
            return 1;
    }
}

int order_continue(elevator_hardware_motor_direction_t direction, int Currfloor){
    switch (direction)
    {
    case DIRN_DOWN:
        return order_get_bottom(Currfloor).set && (order_get_bottom(Currfloor).floor < Currfloor);
    case DIRN_UP:
        return order_get_top(Currfloor).set && (order_get_top(Currfloor).floor > Currfloor);
    
    default:
        return 0;
    }
}