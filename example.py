from ctypes import *
from ctypes.util import find_library

heis = cdll.LoadLibrary("poheis/fsm.so")
heis.elevator_hardware_init()
heis.fsm_init()

while(1):
    heis.fsm_run()
    # elev.elevator_hardware_set_motor_direction(-1)
    # while(elev.elevator_hardware_get_floor_sensor_signal() != 0):
    #     pass
    # elev.elevator_hardware_set_motor_direction(1)
    # while(elev.elevator_hardware_get_floor_sensor_signal() != 3):
    #     pass
    # if(elev.elevator_hardware_get_stop_signal()):
    #     breake