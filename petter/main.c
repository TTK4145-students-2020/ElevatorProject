#include <stdio.h>
#include <stdlib.h>
#include "driver/elevator_hardware.h"
#include "timer.h"
#include "order.h"
#include "fsm.h"

int main(){
    elevator_hardware_init();

    printf("=== Elevator initializing ===\n\r");

    fsm_init();

    printf("=== Elevator running ===\n\r");

    fsm_run();

}
