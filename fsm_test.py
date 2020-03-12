from ctypes import *
from ctypes.util import find_library

heis = cdll.LoadLibrary("petter/driver.so")
heis.main()

while(1):
    pass