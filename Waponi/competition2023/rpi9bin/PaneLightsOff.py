#!/usr/bin/python

# Import libraries
import RPi.GPIO as GPIO
import time
import datetime
from time import sleep

# Pinouts from RPi Zero 2 W
# 22 Panel on		24 LepiLED on
# 27 Panel off		23 LepiLED off

# Set up pin for latching relay FOR THE PANEL OFF
GPIO.setmode(GPIO.BCM)
# Latching Relay #2
GPIO.setup(27, GPIO.OUT)

# Pin 27 turns PANEL off
GPIO.output(27, 1)
sleep(0.1)
GPIO.output(27, 0)

# Reset the pin
GPIO.cleanup(27)

# Make an entry in the logfile
nowdate = datetime.datetime.now()
nowsec = round(time.time())

outfile = open("/home/arducam/rpi9.csv", "a")
curtim = nowdate.strftime("RPi9, Panel_Off, %a %d %b %H:%M:%S %Y, ") 
newlin = " \n"
outfile.write(curtim + str(nowsec) + newlin)
outfile.close()

