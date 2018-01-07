# -*- coding: utf-8 -*-
# Copyright (c) 2018 Steven P. Goldsmith
# See LICENSE.md for details.

"""
Simple callback using built in button
-------------
Since AIOAddGPIOCallback takes a C function pointer Swig generates unusable
code which is ignored in armbianio.i. Another issue it that a GPIOThread
is created trying to write a C wrapper calling a Python function causes
segfaults. The work around is to use Pythons ctypes module. This is way
better then the wiringPi wrapper that has a function for each pin!

Note: Stick with ctypes and do not mix armbianio wrapper module with ctypes
since they are not interchangeable at runtime.  
"""

import time
from ctypes import CFUNCTYPE, CDLL

# Simple callback displays pin and value
def buttonCallback(iPin, iValue):
    print "Button state: pin = %d, value = %d" % (iPin, iValue)

armbianioLib = CDLL("/usr/local/lib/_armbianio.so")
rc = armbianioLib.AIOInit()
if rc == 1:
    print "Running on a %s" % armbianioLib.AIOGetBoardName();
    if armbianioLib.AIOHasButton():
        button = 0
        # Callback prototype
        cfunc = CFUNCTYPE(None, c_int, c_int)
        # Button callback
        armbianioLib.AIOAddGPIOCallback(button, EDGE_BOTH, cfunc(buttonCallback));
        print "Press/release button a few times"
        time.sleep(10)
        armbianioLib.AIORemoveGPIO(0)
    else:
        print "%s does not have a button" % armbianioLib.AIOGetBoardName();
    armbianioLib.AIOShutdown()
else:
    print "AIOInit error"
    