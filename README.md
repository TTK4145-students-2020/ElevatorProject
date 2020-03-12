# ElevatorProject

command to compile fsm:
gcc --std=gnu11 -shared -fPIC timer.c order.c fsm.c main.c driver/elevator_hardware.c -o driver.so /usr/lib/libcomedi.so

på petter sin pc: 
gcc --std=gnu11 -shared -fPIC timer.c order.c fsm.c main.c driver/elevator_hardware.c -o driver.so /usr/local/lib/libcomedi.so