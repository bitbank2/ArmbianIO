# -*- coding: utf-8 -*-
# Copyright (c) 2018 Steven P. Goldsmith
# See LICENSE.md for details.

"""
SPI loopback test
-------------
This should work the same on all SBCs supported by ArmbianIO. Make sure SPI is
configured and wire MO to MI.

Note: Stick with ctypes and do not mix armbianio wrapper module with ctypes
since they are not interchangeable at runtime.
"""

import time
from ctypes import CDLL, c_char_p

armbianioLib = CDLL("/usr/local/lib/_armbianio.so")
# Detect SBC
rc = armbianioLib.AIOInit()
if rc == 1:
    # Function returns char array
    armbianioLib.AIOGetBoardName.restype = c_char_p
    print "Running on a %s" % armbianioLib.AIOGetBoardName();
    # This works on a NanoPi Duo using /dev/spidev1.0, change as needed
    handle = armbianioLib.AIOOpenSPI(1, 500000)
    writeStr = "Test worked!"
    # readStr is different to make sure it is overwritten
    readStr = "012345678901"
    xfer = armbianioLib.AIOReadWriteSPI(handle, writeStr, readStr, len(writeStr))
    print "%d bytes transferred to/from SPI: %s" % (xfer, readStr)
    armbianioLib.AIOCloseSPI(handle)
    armbianioLib.AIOShutdown()
else:
    print "AIOInit error"
