# -*- coding: utf-8 -*-
# Copyright (c) 2018 Steven P. Goldsmith
# See LICENSE.md for details.

"""
Ultrasonic Sensor HC-SR04 using callback
-------------
Distance will not be super accurate due to the nature of not using a realtime
OS. This will not be an issue for a lot of applications. You will notice it
works better bouncing sound off flat surfaces. Testing with people, etc. will
yield some weird values. I used a NanoPi Duo for testing and wired echo to
IRRX and trig to IOG11. You can use a moving average and toss out of bound
values to get more accurate readings. Search around and you will find out
how. This program uses very little CPU.
"""

import time
from ctypes import *
from armbianio.armbianio import GPIO_IN, GPIO_OUT, EDGE_FALLING, EDGE_RISING, EDGE_BOTH

# Trigger pin (IOG11)
trig = 12
# Echo pin (IRRX)
echo = 10
startTime = 0.0
stopTime = 0.0
waiting = False


# Handle echo rising and falling
def echoCallback(iPin, iValue):
    # If rising then save start time
    if iValue == EDGE_RISING:
        global startTime
        startTime = time.time()
    # Falling, so get stop time and calculate inches
    else:
        global stopTime
        stopTime = time.time()
        # Inches here my friends, so don't do a Mars probe gimmick
        distance = (stopTime - startTime) * 6752
        # If value out of range then do not print (13 feet max)
        if distance < 156:
            print "%.2f inches" % distance
        global waiting
        waiting = False


def startPing():
    global waiting
    waiting = True
    # Start with falling value
    armbianioLib.AIOWriteGPIO(trig, EDGE_FALLING)
    time.sleep(0.000002)
    # Set to rising for at least 10 microseconds
    armbianioLib.AIOWriteGPIO(trig, EDGE_RISING)
    time.sleep(0.00001)
    # Set to falling to start sound ping
    armbianioLib.AIOWriteGPIO(trig, EDGE_FALLING)


# Load shared library built with Swig
armbianioLib = CDLL("/usr/local/lib/_armbianio.so")
# Detect SBC
rc = armbianioLib.AIOInit()
if rc == 1:
    # Function returns char array
    armbianioLib.AIOGetBoardName.restype = c_char_p
    print "Running on a %s" % armbianioLib.AIOGetBoardName();
    # Set pin directions
    armbianioLib.AIOAddGPIO(trig, GPIO_OUT)
    armbianioLib.AIOAddGPIO(echo, GPIO_IN)
    # Callback prototype
    cfunc = CFUNCTYPE(None, c_int, c_int)
    # Button callback
    armbianioLib.AIOAddGPIOCallback(echo, EDGE_BOTH, cfunc(echoCallback));
    count = 0
    while count < 100:
        startPing()
        # Sleep while waiting for callback to process
        while waiting:
            time.sleep(0.3)
        count += 1
    # Let last ping finish
    time.sleep(1)
    armbianioLib.AIOShutdown()
else:
    print "AIOInit error"
