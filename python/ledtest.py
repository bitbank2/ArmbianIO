import time
from armbianio.armbianio import *

rc = AIOInit()
if rc == 1:
    AIOAddGPIO(12, GPIO_OUT)
    AIOWriteGPIO(12, 0)
    time.sleep(3)
    AIOWriteGPIO(12, 1)
    AIOShutdown()
else:
    print "AIOInit error"
