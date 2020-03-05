#include "order.h"

/**
 * @brief Creates an 4x3 order matrix, which we access to handle orders.
 */
static order_t m_orderMatrix[HARDWARE_NUMBER_OF_FLOORS][HARDWARE_ORDER_TYPES];


int order_add(order_t order){

    order.set = 1;
    m_orderMatrix[order.floor][order.orderType] = order;
    
    return 0;
}

int order_poll_buttons(void){

    order_t order;

    for(int i = 0; i < HARDWARE_NUMBER_OF_FLOORS; i++){

        if(hardware_read_order(i, HARDWARE_ORDER_INSIDE)){
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

    for (int j = 0; j < HARDWARE_ORDER_TYPES; j++){
        m_orderMatrix[floor][j].set = 0;
        hardware_command_order_light(floor, j, 0);   
    }
    return 0;
}

void order_clear_all(void){

    for (int i = 0; i < HARDWARE_NUMBER_OF_FLOORS; i++){

        for (int j = 0; j < HARDWARE_ORDER_TYPES; j++){
                m_orderMatrix[i][j].set = 0;
                hardware_command_order_light(i, j, 0);
        }
    }
}

int order_is_set(int floor){

    for(int i = 0; i < HARDWARE_ORDER_TYPES; i++){

        if(m_orderMatrix[floor][i].set){
            return 1;
        }
    }
    return 0;
}

order_t order_get_top(int floor){

    order_t order = m_orderMatrix[HARDWARE_NUMBER_OF_FLOORS][HARDWARE_ORDER_TYPES];

    for(int i = floor; i < HARDWARE_NUMBER_OF_FLOORS; i++){

        for (int j = 0; j < HARDWARE_ORDER_TYPES; j++){

            if(m_orderMatrix[i][j].set == true){
                order = m_orderMatrix[i][j];
            }
        }
    }

    return order;
}

order_t order_get_bottom(int floor){

    order_t order = m_orderMatrix[0][HARDWARE_ORDER_TYPES];

    for(int i = floor; i > -1; i--){

        for (int j = 0; j < HARDWARE_ORDER_TYPES; j++){

            if(m_orderMatrix[i][j].set == true){
                order = m_orderMatrix[i][j];
            }
        }
    }
 
    return order;
}



int order_stop_at_floor(HardwareMovement direction, int currentFloor){

    switch(direction){

        case HARDWARE_MOVEMENT_DOWN:
            return m_orderMatrix[currentFloor][HARDWARE_ORDER_DOWN].set
            || m_orderMatrix[currentFloor][HARDWARE_ORDER_INSIDE].set
            || ((order_get_bottom(currentFloor).floor == currentFloor) && order_get_bottom(currentFloor).set)
            || currentFloor == 0;

        case HARDWARE_MOVEMENT_UP:
            return m_orderMatrix[currentFloor][HARDWARE_ORDER_UP].set
            || m_orderMatrix[currentFloor][HARDWARE_ORDER_INSIDE].set
            || ((order_get_top(currentFloor).floor == currentFloor) && order_get_top(currentFloor).set)
            || currentFloor == HARDWARE_NUMBER_OF_FLOORS-1;

        default:
            return 1;
    }
}

int order_continue(HardwareMovement direction, int currentFloor){

    switch (direction){

    case HARDWARE_MOVEMENT_DOWN:
        return order_get_bottom(currentFloor).set && (order_get_bottom(currentFloor).floor < currentFloor);

    case HARDWARE_MOVEMENT_UP:
        return order_get_top(currentFloor).set && (order_get_top(currentFloor).floor > currentFloor);
    
    default:
        return 0;
    }
}