# ElevatorProject

### Running several elevators with the simulator
- run simulator in one terminal and "run_elevator_2()" from main.py in another.
- change the last number of the port in simulator.con
- change the port number in elevator_hardware.c 
- run the compile command below
- same as 1 but running "run_elvator_1()" instead.

run fsm.py file after compiling with the command below to run with one elevator.

**Command to compile drivers to use python fsm and order module, must be run in the folder "petter":**
gcc --std=gnu11 -shared -fPIC timer.c driver/elevator_hardware.c -o driver.so /usr/local/lib/libcomedi.so

**if its not working, try:**
gcc --std=gnu11 -shared -fPIC timer.c driver/elevator_hardware.c -o driver.so /usr/lib/libcomedi.so









### OUTDATED:
command to compile fsm:
gcc --std=gnu11 -shared -fPIC timer.c order.c fsm.c main.c driver/elevator_hardware.c -o driver.so /usr/lib/libcomedi.so

på petter sin pc: 
gcc --std=gnu11 -shared -fPIC timer.c order.c fsm.c main.c driver/elevator_hardware.c -o driver.so /usr/local/lib/libcomedi.so



