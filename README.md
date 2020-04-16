# ElevatorProject

### Running several elevators with the simulator
- run simulator in one terminal and main.py in another.
- change ELEV_ID in config.py (starting ID is 0)
- change the last number of the port in simulator.con 
- change the port number in elevator_hardware.c (port has to be the same as above)
- run the compile command below
- now run a second simulator in a new terminal and main.py in another

**Command to compile drivers to use python fsm and order module, must be run in the folder "petter":**
gcc --std=gnu11 -shared -fPIC timer.c driver/elevator_hardware.c -o driver.so /usr/local/lib/libcomedi.so

**if its not working, try:**
gcc --std=gnu11 -shared -fPIC timer.c driver/elevator_hardware.c -o driver.so /usr/lib/libcomedi.so


sudo iptables -A INPUT -p tcp --dport 15657 -j ACCEPT
sudo iptables -A INPUT -p tcp --sport 15657 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 15658 -j ACCEPT
sudo iptables -A INPUT -p tcp --sport 15658 -j ACCEPT

sudo iptables -A INPUT -j DROP

sudo iptables -F



### OUTDATED:
command to compile fsm:
gcc --std=gnu11 -shared -fPIC timer.c order.c fsm.c main.c driver/elevator_hardware.c -o driver.so /usr/lib/libcomedi.so

på petter sin pc: 
gcc --std=gnu11 -shared -fPIC timer.c order.c fsm.c main.c driver/elevator_hardware.c -o driver.so /usr/local/lib/libcomedi.so



