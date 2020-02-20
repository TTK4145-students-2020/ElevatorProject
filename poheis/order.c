#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "hardware.h"
#include "order.h"

int order_add(order_t order){
    order.set = true;
    orderQueue[order.floor][order.orderType] = order;
    return 0;
}

int order_poll(void){
    order_t order;
    for(int i = 0; i < HARDWARE_NUMBER_OF_FLOORS; i++){
        if(hardware_read_order(i, HARDWARE_ORDER_INSIDE)){
            //printf("%d\n\r", i);
            order.floor = i;
            order.orderType = HARDWARE_ORDER_INSIDE;
            order.set = 1;
            order_add(order);
            hardware_command_order_light(i,HARDWARE_ORDER_INSIDE, 1);
        }
        if(hardware_read_order(i, HARDWARE_ORDER_DOWN)){
            order.floor = i;
            order.orderType = HARDWARE_ORDER_DOWN;
            order.set = 1;
            order_add(order);
            hardware_command_order_light(i, HARDWARE_ORDER_DOWN, 1);
        }
        if(hardware_read_order(i, HARDWARE_ORDER_UP)){
            order.floor = i;
            order.orderType = HARDWARE_ORDER_UP;
            order.set = 1;
            order_add(order);
            hardware_command_order_light(i, HARDWARE_ORDER_UP, 1);
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



int order_stop_at_floor(HardwareMovement direction, int Currfloor){
    switch(direction){
        case HARDWARE_MOVEMENT_DOWN:
            return orderQueue[Currfloor][HARDWARE_ORDER_DOWN].set || orderQueue[Currfloor][HARDWARE_ORDER_INSIDE].set || ((order_get_bottom(Currfloor).floor == Currfloor) && order_get_bottom(Currfloor).set) || Currfloor == 0;
        case HARDWARE_ORDER_UP:
            return orderQueue[Currfloor][HARDWARE_ORDER_UP].set || orderQueue[Currfloor][HARDWARE_ORDER_INSIDE].set || ((order_get_top(Currfloor).floor == Currfloor) && order_get_top(Currfloor).set) || Currfloor == HARDWARE_NUMBER_OF_FLOORS-1;

        default:
            return 1;
    }
}

int order_continue(HardwareMovement direction, int Currfloor){
    switch (direction)
    {
    case HARDWARE_MOVEMENT_DOWN:
        return order_get_bottom(Currfloor).set && (order_get_bottom(Currfloor).floor < Currfloor);
    case HARDWARE_MOVEMENT_UP:
        return order_get_top(Currfloor).set && (order_get_top(Currfloor).floor > Currfloor);
    
    default:
        return 0;
    }
}