#include "order.h"

/**
 * @brief Creates an 4x3 order matrix, which we access to handle orders.
 */

static order_t m_orderMatrix[N_FLOORS][N_ELEVATORS];

order_t order_get_order_matrix(int floor, int elev_id){
    printf("%d\n\r", m_orderMatrix[floor][elev_id].set);
    return m_orderMatrix[floor][elev_id];
}


//endre denne til å kunne legge til i alle heisers ordreliste, må ta inn elev_id
int order_add(order_t order){
    order.set = 1;
    m_orderMatrix[order.floor][ELEV_ID] = order;
    
    return 0;
}

int order_poll_buttons(void){

    order_t order;

    for(int i = 0; i < N_FLOORS; i++){
        if(elevator_hardware_get_button_signal(BUTTON_COMMAND, i)){
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
            elevator_hardware_set_button_lamp(BUTTON_CALL_DOWN, i, 1);;
        }
        if(elevator_hardware_get_button_signal(BUTTON_CALL_UP, i)){
            order.floor = i;
            order.orderType = BUTTON_CALL_UP;
            order.set = 1;
            order_add(order);
            elevator_hardware_set_button_lamp(BUTTON_CALL_UP, i, 1);;
        }
    }
    return 0;
}

int order_clear_floor(int floor){

    for (int j = 0; j < N_BUTTONS; j++){
        m_orderMatrix[floor][ELEV_ID].set = 0;
        elevator_hardware_set_button_lamp(j, floor, 0);  
    }
    return 0;
}

void order_clear_all(void){

    for (int i = 0; i < N_FLOORS; i++){

        for (int j = 0; j < N_BUTTONS; j++){
                m_orderMatrix[i][ELEV_ID].set = 0;
                elevator_hardware_set_button_lamp(j, i, 0);;
        }
    }
}

int order_is_set(int floor){

    for(int i = 0; i < N_ELEVATORS; i++){

        if(m_orderMatrix[floor][i].set){
            return 1;
        }
    }
    return 0;
}

order_t order_get_top(int floor){

    order_t order = m_orderMatrix[N_FLOORS][ELEV_ID];

    for(int i = floor; i < N_FLOORS; i++){

        for (int j = 0; j < N_BUTTONS; j++){

            if(m_orderMatrix[i][ELEV_ID].set == true){
                order = m_orderMatrix[i][ELEV_ID];
            }
        }
    }

    return order;
}

order_t order_get_bottom(int floor){

    order_t order = m_orderMatrix[0][ELEV_ID];

    for(int i = floor; i > -1; i--){

        for (int j = 0; j < N_BUTTONS; j++){

            if(m_orderMatrix[i][ELEV_ID].set == true){
                order = m_orderMatrix[i][ELEV_ID];
            }
        }
    }
 
    return order;
}



int order_stop_at_floor(elevator_hardware_motor_direction_t direction, int currentFloor){

    switch(direction){

        case DIRN_DOWN:
            return (m_orderMatrix[currentFloor][ELEV_ID].set && m_orderMatrix[currentFloor][ELEV_ID].orderType == BUTTON_CALL_DOWN)
            || (m_orderMatrix[currentFloor][ELEV_ID].set && m_orderMatrix[currentFloor][ELEV_ID].orderType == BUTTON_COMMAND)
            || ((order_get_bottom(currentFloor).floor == currentFloor) && order_get_bottom(currentFloor).set)
            || currentFloor == 0;

        case DIRN_UP:
            return (m_orderMatrix[currentFloor][ELEV_ID].set && m_orderMatrix[currentFloor][ELEV_ID].orderType == BUTTON_CALL_UP)
            || (m_orderMatrix[currentFloor][ELEV_ID].set && m_orderMatrix[currentFloor][ELEV_ID].orderType == BUTTON_COMMAND)
            || ((order_get_top(currentFloor).floor == currentFloor) && order_get_top(currentFloor).set)
            || currentFloor == N_FLOORS-1;

        default:
            return 1;
    }
}

int order_continue(elevator_hardware_motor_direction_t direction, int currentFloor){

    switch (direction){

    case DIRN_DOWN:
        return order_get_bottom(currentFloor).set && (order_get_bottom(currentFloor).floor < currentFloor);

    case DIRN_UP:
        return order_get_top(currentFloor).set && (order_get_top(currentFloor).floor > currentFloor);
    
    default:
        return 0;
    }
}