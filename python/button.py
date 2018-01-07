# -*- coding: utf-8 -*-
# Copyright (c) 2018 Steven P. Goldsmith
# See LICENSE.md for details.

"""
Simple callback using built in button
-------------
Since AIOAddGPIOCallback takes a C function pointer Swig generates unusable
code which is ignored in armbianio.i. Another issue is that a GPIOThread
is created, so trying to write a C wrapper calling a Python function causes
segfaults. The work around is to use Python's ctypes module. This is way
better than the wiringPi wrapper that has a huge switch statement!

Note: Stick with ctypes and do not mix armbianio wrapper module with ctypes
since they are not interchangeable at runtime. I'm only using Swig wrapper
for the EDGE_BOTH constant.
"""

import time
from ctypes import *
from armbianio.armbianio import EDGE_BOTH

# Simple callback displays pin and value
def buttonCallback(iPin, iValue):
    print "Button state: pin = %d, value = %d" % (iPin, iValue)

armbianioLib = CDLL("/usr/local/lib/_armbianio.so")
# Detect SBC
rc = armbianioLib.AIOInit()
if rc == 1:
    # Function returns char array
    armbianioLib.AIOGetBoardName.restype = c_char_p
    print "Running on a %s" % armbianioLib.AIOGetBoardName();
    if armbianioLib.AIOHasButton():
        button = 0
        # Callback prototype
        cfunc = CFUNCTYPE(None, c_int, c_int)
        # Button callback
        armbianioLib.AIOAddGPIOCallback(button, EDGE_BOTH, cfunc(buttonCallback));
        print "Press/release button a few times\n"
        time.sleep(10)
        armbianioLib.AIORemoveGPIO(0)
    else:
        print "%s does not have a button" % armbianioLib.AIOGetBoardName();
    armbianioLib.AIOShutdown()
else:
    print "AIOInit error"
