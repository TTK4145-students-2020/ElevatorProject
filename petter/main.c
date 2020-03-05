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

    printf("=== Elevator initializing ===\n\r");

    fsm_init();

    printf("=== Elevator running ===\n\r");

    fsm_run();

}
