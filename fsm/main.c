#include <stdio.h>
#include <stdlib.h>
#include "hardware.h"
#include "timer.h"
#include "order.h"
#include "fsm.h"

int main(){
    int error = hardware_init();
    if(error != 0){
        fprintf(stderr, "Unable to initialize hardware\n");
        exit(1);
    }

    printf("=== Example Program ===\n");
    printf("Press the stop button on the elevator panel to exit\n\r");

    //hardware_command_movement(HARDWARE_MOVEMENT_UP);
    fsm_init();
    fsm_run();
//     while(1){
//         if(hardware_read_stop_signal()){
//             printf("stop button pressed\r\n"); 
//             hardware_command_movement(HARDWARE_MOVEMENT_STOP);
//             break;
//         }
// /*
//         if(hardware_read_floor_sensor(0)){
//             hardware_command_movement(HARDWARE_MOVEMENT_UP);
//         }
//         if(hardware_read_floor_sensor(HARDWARE_NUMBER_OF_FLOORS - 1)){
//             hardware_command_movement(HARDWARE_MOVEMENT_DOWN);
//         }
// */
        
//         if(hardware_read_order(1, HARDWARE_ORDER_INSIDE)){ //leser etasje 2 heispanel
//             order_t order;
//             order.floor = 1;
//             order.orderType = 1;
//             order_t order1;
//             order1.floor = 2;
//             order1.orderType = 1;

//             order_add(order);
//             order_add(order1);
//             order_clear_floor(2);
//             order_t retOrd = order_get_bottom(3);
//             printf("Floor: %d\tType: %d\r\n",retOrd.floor, retOrd.orderType);
//         }
//     }
}
