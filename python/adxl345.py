# -*- coding: utf-8 -*-
# Copyright (c) 2018 Steven P. Goldsmith
# See LICENSE.md for details.

"""
ADXL345 3-Axis, ±2 g/±4 g/±8 g/±16 g digital accelerometer 
-------------
I'm using I2C to communicate with the ADXL345 although SPI is supported as
well.

Note: Stick with ctypes and do not mix armbianio wrapper module with ctypes
since they are not interchangeable at runtime.
"""

import time
from armbianio.armbianio import *

def getRange(handle):
    """Retrieve the current range of the accelerometer.  See setRange for
    the possible range constant values that will be returned.
    """
    retVal = "0"
    AIOReadI2C(handle, 0x31, retVal, 1)
    return ord(retVal) & 0x03

def setRange(handle, value):
    """Set the range of the accelerometer to the provided value.
    """
    # Read the data format register to preserve bits.  Update the data
    # rate, make sure that the FULL-RES bit is enabled for range scaling
    retVal = "0"
    AIOReadI2C(handle, 0x31, retVal, 1)
    formatReg = ord(retVal) & ~0x0f
    formatReg |= value
    formatReg |= 0x08  # FULL-RES bit enabled
    # Write the updated format register
    AIOWriteI2C(handle, 0x31, chr(formatReg), 1)

def setDataRate(handle, rate):
    """Set the data rate of the accelerometer.
    """
    # Note: The LOW_POWER bits are currently ignored,
    # we always keep the device in 'normal' mode
    AIOWriteI2C(handle, 0x2c, chr(rate & 0x0f), 1)
   
def getDataRate(handle):
    """Retrieve the current data rate.
    """
    retVal = "0"
    AIOReadI2C(handle, 0x2c, retVal, 1)
    return ord(retVal) & 0x0f

def intFix(value):
    if value > 32767:
        value -= 65535
    return value

def read(handle):
    """Retrieve the current data rate. X-axis data 0 (6 bytes for X/Y/Z).
    """
    retVal = "012345"
    AIOReadI2C(handle, 0x32, retVal, len(retVal))
    # Convert string to tuple of 16 bit integers x, y, z
    x = ord(retVal[0]) | (ord(retVal[1]) << 8)
    if(x & (1 << 16 - 1)):
        x = x - (1<<16)
    y = ord(retVal[2]) | (ord(retVal[3]) << 8)
    if(y & (1 << 16 - 1)):
        y = y - (1<<16)
    z = ord(retVal[4]) | (ord(retVal[5]) << 8)
    if(z & (1 << 16 - 1)):
        z = z - (1<<16)    
    return (x, y, z)

# Detect SBC
rc = AIOInit()
if rc == 1:
    print "Running on a %s" % AIOGetBoardName();
    # ADXL345 wired up to NanoPi Duo i2c-0 on port 0x53
    handle = AIOOpenI2C(0, 0x53)
    deviceId = "0"
    if AIOReadI2C(handle, 0x00, deviceId, 1) > 0:
        # Is this an ADXL345?
        if hex(ord(deviceId)) == "0xe5":
            # Enable the accelerometer
            if AIOWriteI2C(handle, 0x2d, chr(0x08), 1) > 0:
                # +/- 2g
                setRange(handle, 0x00)
                # 100 Hz
                setDataRate(handle, 0x0a)
                print "Range = %d, data rate = %d" % (getRange(handle), getDataRate(handle))
                count = 0
                while count < 1000:
                    data = read(handle)
                    print "x: %04d, y: %04d, z: %04d" % (data[0], data[1], data[2])
                    time.sleep(0.5)
                    count += 1
        else:
            print "Failed to find the expected device ID register value, check your wiring and I2C configuration"
    AIOCloseI2C(handle)
    AIOShutdown()
else:
    print "AIOInit error"
