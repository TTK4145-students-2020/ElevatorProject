from ctypes import *
from ctypes.util import find_library
import Network
import json
from threading import Thread

heis = cdll.LoadLibrary("petter/driver.so")

p1 = Thread(target = heis.main)
p2 = Thread(target =heis.order_get_order_matrix, args=(1, 1,))
p2.start()
p1.start()
while True:
    p2.join()
    p1.join()
