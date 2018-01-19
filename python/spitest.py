# -*- coding: utf-8 -*-
# Copyright (c) 2018 Steven P. Goldsmith
# See LICENSE.md for details.

"""
SPI loopback test
-------------
This should work the same on all SBCs supported by ArmbianIO. Make sure SPI is
configured and wire MO to MI.

"""

import time
from armbianio.armbianio import *

# Detect SBC
rc = AIOInit()
if rc == 1:
    print "Running on a %s" % AIOGetBoardName();
    # This works on a NanoPi Duo using /dev/spidev1.0, change as needed
    handle = AIOOpenSPI(1, 500000)
    writeStr = "Test worked!"
    # readStr is different to make sure it is overwritten
    readStr = "012345678901"
    xfer = AIOReadWriteSPI(handle, writeStr, readStr, len(writeStr))
    print "%d bytes transferred to/from SPI: %s" % (xfer, readStr)
    AIOCloseSPI(handle)
    AIOShutdown()
else:
    print "AIOInit error"
