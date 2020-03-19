# ElevatorProject

run fsm.py file after compiling with the command below.


**Command to compile drivers to use python fsm and order module, must be run in the folder "petter":**
gcc --std=gnu11 -shared -fPIC timer.c driver/elevator_hardware.c -o driver.so /usr/local/lib/libcomedi.so

**if its not working, try:**
gcc --std=gnu11 -shared -fPIC timer.c driver/elevator_hardware.c -o driver.so /usr/lib/libcomedi.so





### OUTDATED:
command to compile fsm:
gcc --std=gnu11 -shared -fPIC timer.c order.c fsm.c main.c driver/elevator_hardware.c -o driver.so /usr/lib/libcomedi.so

på petter sin pc: 
gcc --std=gnu11 -shared -fPIC timer.c order.c fsm.c main.c driver/elevator_hardware.c -o driver.so /usr/local/lib/libcomedi.so



