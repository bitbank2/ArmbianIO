# -*- coding: utf-8 -*-
# Copyright (c) 2018 Steven P. Goldsmith
# See LICENSE.md for details.

"""
Sonar using Ultrasonic Sensor HC-SR04
-------------
Distance will not be super accurate due to the nature of not using a realtime
OS. This will not be an issue for a lot of applications. You will notice it
works better bouncing sound off flat surfaces. Testing with people, etc. will
yield some weird values. I used a NanoPi Duo for testing and wired echo to
pin 10 (IRRX) and trig to pin 12 (IOG11). Uses a moving average and tosses
out of bound values to get more accurate readings.

Pass the configuration file name as an argument or sonar.ini will be used.
Use minTrip and maxTrip values to define a range where you should trip an
event. You just need to implement code to do something. Right now it just
logs the value that caused the trip. If the HC-SR04 does not receive an echo
then the output never goes low. This will not hang the program since it
is using a callback to drive sampling. 

Note: Stick with ctypes and do not mix armbianio wrapper module with ctypes
since they are not interchangeable at runtime. I'm only using Swig wrapper
for the constants.
"""

import ConfigParser, logging, sys, os, traceback, time, datetime
from ctypes import CDLL, CFUNCTYPE, c_int, c_char_p
from armbianio.armbianio import GPIO_IN, GPIO_OUT, EDGE_FALLING, EDGE_RISING, EDGE_BOTH

class sonar:

    def __init__(self, fileName):
        """Read in configuration and load shared library"""
        self.parser = ConfigParser.SafeConfigParser()
        # Read configuration file
        self.parser.read(fileName)
        # Set up logger
        self.logger = logging.getLogger("sonar")
        self.logger.setLevel(self.parser.get("logging", "level"))
        formatter = logging.Formatter(self.parser.get("logging", "formatter"))
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info("Configuring from file: %s" % fileName)
        self.logger.info("Logging level: %s" % self.parser.get("logging", "level"))
        self.logger.debug("Logging formatter: %s" % self.parser.get("logging", "formatter"))
        self.risingTime = 0.0
        self.fallingTime = 0.0
        # Load shared library built with Swig
        self.armbianioLib = CDLL(self.parser.get("gpio", "dll"))
        self.triggerPin = self.parser.getint("gpio", "triggerPin")
        self.echoPin = self.parser.getint("gpio", "echoPin")
        self.samples = self.parser.getint("distance", "samples")
        self.delay = self.parser.getfloat("distance", "delay")
        self.unitsPerSec = self.parser.getint("distance", "unitsPerSec")
        self.minRange = self.parser.getint("distance", "minRange")
        self.maxRange = self.parser.getint("distance", "maxRange")
        self.minTrip = self.parser.getint("distance", "minTrip")
        self.maxTrip = self.parser.getint("distance", "maxTrip")
        self.waiting = False
        self.sample = 0
        self.totalDist = 0.0
        
    def echoCallback(self, pin, value):
        """Handle echo rising and falling"""
        # If rising then save time
        if value == EDGE_RISING:
            self.risingTime = time.time()
        # Falling, so calculate distance
        else:
            self.fallingTime = time.time()
            # Calculate distance
            distance = (self.fallingTime - self.risingTime) * self.unitsPerSec
            # If value out of range then reject sample
            if distance > self.minRange and distance < self.maxRange:
                self.sample += 1
                self.totalDist += distance
            else:
                self.logger.debug("Out of range: %0.2f" % distance)
            self.waiting = False

    def configDevice(self):
        """Set pin directions and echo callback"""
        # Set pin directions
        self.armbianioLib.AIOAddGPIO(self.triggerPin, GPIO_OUT)
        self.armbianioLib.AIOAddGPIO(self.echoPin, GPIO_IN)
        # Keep reference from being garbage collected and getting Segmentation fault
        self.callback = self.echoCallback
        # Callback prototype (use self to keep reference)
        self.cfunc = CFUNCTYPE(None, c_int, c_int)
        # Echo callback
        self.armbianioLib.AIOAddGPIOCallback(self.echoPin, EDGE_BOTH, self.cfunc(self.callback));

    def ping(self):
        """Ping with sound"""
        # Start with falling value
        self.armbianioLib.AIOWriteGPIO(self.triggerPin, EDGE_FALLING)
        time.sleep(0.000002)
        # Set to rising for at least 10 microseconds
        self.armbianioLib.AIOWriteGPIO(self.triggerPin, EDGE_RISING)
        time.sleep(0.00001)
        # Set to falling to start sound ping
        self.armbianioLib.AIOWriteGPIO(self.triggerPin, EDGE_FALLING)

    def loop(self):
        """Calculate distance """
        while True:
            self.startTime = time.time()
            self.waiting = True
            self.ping()
            if self.waiting:
                sleepTime = self.delay - (time.time() - self.startTime)
                if sleepTime > 0:
                    time.sleep(sleepTime)
            if self.sample >= self.samples:
                distance = self.totalDist / self.sample
                # See if we should trip some type of event
                if distance > self.minTrip and distance < self.maxTrip:
                    self.logger.info("Trip distance: %0.2f" % (self.totalDist / self.sample))
                self.logger.debug("Average distance: %0.2f" % (self.totalDist / self.sample))
                self.sample = 0
                self.totalDist = 0.0

if __name__ == "__main__":
    try:
        # sys.argv[1] is configuration file or default is used
        if len(sys.argv) < 2:
            fileName = "sonar.ini"
        else:
            fileName = os.path.expanduser(sys.argv[1])
        sonar = sonar(fileName)
        # Detect SBC
        rc = sonar.armbianioLib.AIOInit()
        if rc == 1:
            # Function returns char array
            sonar.armbianioLib.AIOGetBoardName.restype = c_char_p
            sonar.logger.info("Running on %s" % sonar.armbianioLib.AIOGetBoardName().rstrip())
            # Set pin directions and echo callback
            sonar.configDevice()
            sonar.loop()
        else:
            sonar.logger.error("SBC not detected")
        # Clean up
        sonar.armbianioLib.AIOShutdown()
    except:
        # Add timestamp to errors
        sys.stderr.write("%s " % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f"))
        traceback.print_exc(file=sys.stderr)
