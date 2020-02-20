from ctypes import *
from ctypes.util import find_library

elev = cdll.LoadLibrary("driver/driver.so")
elev.elevator_hardware_init()

while(1):
    elev.elevator_hardware_set_motor_direction(-1)
    while(elev.elevator_hardware_get_floor_sensor_signal() != 0):
        pass
    elev.elevator_hardware_set_motor_direction(1)
    while(elev.elevator_hardware_get_floor_sensor_signal() != 3):
        pass
    if(elev.elevator_hardware_get_stop_signal()):
        break
#print(find_library("driver/"))