from ctypes import *
from ctypes.util import find_library

heis = cdll.LoadLibrary("ProjectResources-master/elev_algo/fsm.so")
heis.main()

while(1):
    pass