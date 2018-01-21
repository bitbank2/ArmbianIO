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
"""

import time
from armbianio.armbianio import *


# Simple callback displays pin and value
def buttonCallback(iPin, iEdge):
    print "Button state: pin = %d, value = %d" % (iPin, iEdge)


# Detect SBC
rc = AIOInit()
if rc == 1:
    print "Running on a %s" % AIOGetBoardName()
    if AIOHasButton():
        AIOAddGPIO(0, GPIO_IN)
        # Button callback
        AIOAddGPIOCallback(0, EDGE_BOTH, AIOCALLBACK(buttonCallback))
        print "Press/release button a few times\n"
        time.sleep(10)
        # Remove callback
        AIORemoveGPIOCallback(0)
        # Remove pin (actually you cannot remove the button)
        AIORemoveGPIO(0)
    else:
        print "%s does not have a button" % AIOGetBoardName()
    AIOShutdown()
else:
    print "AIOInit error"
