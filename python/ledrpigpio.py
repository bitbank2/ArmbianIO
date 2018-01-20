# -*- coding: utf-8 -*-
# Copyright (c) 2018 Steven P. Goldsmith
# See LICENSE.md for details.

"""
Simple LED blink using RPi.GPIO wrapper
-------------
Using the NanoPi Duo connect a 220Ω resistor to the anode (the long pin of
the LED), then the resistor to 3.3 V, and connect the cathode (the short
pin) of the LED to pin 12 (IOG11). The anode of LED connects to a
current-limiting resistor and then to 3.3V. Therefore, to turn on an LED,
we need to make pin 12 low (0V) level. It can be realized by programming.
See images/ledtest.jpg for schematic.
"""

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# Pin 12 set to output
GPIO.setup(12,GPIO.OUT)
# LED on
GPIO.output(12,GPIO.LOW)
time.sleep(3)
# LED off
GPIO.output(12,GPIO.HIGH)
GPIO.cleanup()
