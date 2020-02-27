#ifndef FSM_H
#define FSM_H

#include "order.h"
#include "timer.h"
#include "driver/elevator_hardware.h"
#include <stdlib.h>
#include <stdio.h>

int fsm_get_current_floor(void);
int fsm_emergency_poll(void);
int fsm_move_towards_current_order(order_t order);
int fsm_init(void);
int fsm_run(void);
int fsm_emergency_stop(void);
int fsm_obstruction_handler(void);
int order_poll(void);

#endif
