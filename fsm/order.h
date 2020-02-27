/**
 * @file
 * @brief Creates an 4x3 order matrix and handles orders.
 */

#ifndef ORDER_H
#define ORDER_H
#include <stdbool.h>
#include "driver/elevator_hardware.h"
#include <stdlib.h>
#include <stdio.h>

#define FLOORS 4
#define orderTypes 3


/**
 * Creates an 4x3 order matrix, which we access to handle orders.
 */
typedef struct order{
    int floor;
    int orderType;
    bool set;
}order_t;

static order_t orderQueue[FLOORS][orderTypes];

/**
 * @brief Struct containing the floor of the order, the type and if its active.
 */



/**
 * @brief Adds order to order matrix.
 * @param order containing @c floor, @c orderType, @c set.
 */
int order_add(order_t order);

/**
 * @brief Polls for orders in all floors and adds them to order matrix.
 */
int order_poll(void);

/**
 * @brief Clears all orders on a floor in order matrix.
 * @param floor to clear.
 */
int order_clear_floor(int floor);

/**
 * @brief Clears all orders in order matrix.
 */
void order_clear_all(void);

/**
 * @return order from a @p floor and of a @p orderType.
 */
int order_get(int floor);

/**
 * @return The topmost order from elevator position.
 * @param floor Elevator position.
 */
order_t order_get_top(int floor);

/**
 * @return The bottommost order from elevator position.
 * @param floor Elevator position.
 */
order_t order_get_bottom(int floor);
//order_t order_get_next(HardwareMovement direction, int prevRegisteredFloor);
int order_stop_at_floor(elevator_hardware_motor_direction_t direction, int floor);
int order_continue(elevator_hardware_motor_direction_t direction, int floor);
#endif
