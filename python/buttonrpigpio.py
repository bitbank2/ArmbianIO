# -*- coding: utf-8 -*-
# Copyright (c) 2018 Steven P. Goldsmith
# See LICENSE.md for details.

"""
Simple callback using built in button using RPi.GPIO wrapper
-------------
Should work on any board with a button built in.
"""

import time
import RPi.GPIO as GPIO


# Simple callback displays channel
def buttonCallback(channel):
    print "Button state: pin = %d, value = %d" % (channel, GPIO.input(channel))

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# Set button to input (sysfs always has button exported)
GPIO.setup(0,GPIO.IN)
print "Press and hold button"
GPIO.wait_for_edge(0, GPIO.FALLING)
print "Button pressed, release button"
GPIO.wait_for_edge(0, GPIO.RISING)
print "Button released, press button a few times"
GPIO.add_event_detect(0, GPIO.BOTH, callback=buttonCallback)
time.sleep(10)
GPIO.remove_event_detect(0)
GPIO.cleanup()