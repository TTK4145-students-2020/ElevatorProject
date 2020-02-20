#include <stdlib.h>
#include <time.h>
#include "timer.h"

int timer_start(void){
    timeVal = time(NULL);
    return 0;
}

int timer_expire(void){

    if (timeVal == -1) return 0;

    else return (time(NULL)- timeVal > timeLimit);
}