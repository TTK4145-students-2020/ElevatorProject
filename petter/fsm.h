/**
 * @file
 * @brief Initializes the FSM and runs the elevator in different states.
 */
#ifndef FSM_H
#define FSM_H

#include "order.h"
#include "timer.h"
#include "hardware.h"
#include <stdlib.h>
#include <stdio.h>

/**
 * @brief @c UNDEFINED State used before the elevator is initialize.
 */
#define UNDEFINED -1
/**
 * @brief @c IDLE State when the elevator is standing still without orders. 
 */
#define IDLE 0
/**
 * @brief @c RUN State for when the elevator is moving and handling orders.
 */
#define RUN 1
/**
 * @brief @c DOOR_OPEN State to clear orders for a floor and opening and closing the door.
 */
#define DOOR_OPEN 2

/**
 * @brief @c EMERGENCY_STOP State for when the emergency button is pressed.
 */
#define EMERGENCY_STOP 3

/**
 * @return The floor the elevator is at.
 */
int fsm_get_current_floor(void);

/**
 * @brief Initializes the elevator to 1st floor, and sets it to @c IDLE state.
 */
int fsm_init(void);

/**
 * @brief Runs the elevator in the different states. 
 */
int fsm_run(void);

#endif
