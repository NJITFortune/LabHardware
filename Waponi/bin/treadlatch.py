#!/usr/bin/python

# Import libraries
import RPi.GPIO as GPIO
from time import sleep

# Set up pins for latching relay
GPIO.setmode(GPIO.BCM)
# Latching Relay #1
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
# Latching Relay #2
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

sleep(1)
# Pin 24 turns Device #1 on
GPIO.output(24, 1)
sleep(0.1)
GPIO.output(24, 0)

sleep(1)
# Pin 22 turns Device #2 on
GPIO.output(22, 1)
sleep(0.1)
GPIO.output(22, 0)

# Set the sleep time to match conveyor speed
sleep(5) 

# Pin 23 turns Device #1 off
GPIO.output(23, 1)
sleep(0.1)
GPIO.output(23, 0)

sleep(1)
# Pin 22 turns Device #2 off
GPIO.output(27, 1)
sleep(0.1)
GPIO.output(27, 0)

# Reset the pins
GPIO.cleanup(23)
GPIO.cleanup(24)
GPIO.cleanup(22)
GPIO.cleanup(27)

