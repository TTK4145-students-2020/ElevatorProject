/**
 * @file
 * @brief Creates an 4x3 order matrix and handles orders.
 */

#ifndef ORDER_H
#define ORDER_H

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "driver/elevator_hardware.h"

/**
 * @brief Struct containing the floor of the order, the type and if its active.
 */
typedef struct order{
    //int ID;
    int floor;
    int orderType;
    int set;
}order_t;

order_t order_get_order_matrix(int floor, int elev_id);

/**
 * @brief Adds order to order matrix.
 * @param order containing @c floor, @c orderType, @c set.
 */
int order_add(order_t order);

/**
 * @brief Polls for orders in all floors and adds them to order matrix.
 */
int order_poll_buttons(void);

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
 * @return 1 if there is a active order on @p floor , zero otherwise.
 */
int order_is_set(int floor);

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

/**
 * @brief Checks if elevator is supposed to stop at a @p floor.
 * @param direction The moving direction of the elevator.
 * @return 1 if it should stop, 0 otherwise.
 */ 
int order_stop_at_floor(elevator_hardware_motor_direction_t direction, int floor);

/**
 * @brief Checks if elevator is supposed to continue doing orders.
 * @param direction The moving direction of the elevator.
 * @param floor The floor the elevator is at.
 * @return 1 if it should continue doing orders.
 */
int order_continue(elevator_hardware_motor_direction_t direction, int floor);
#endif
