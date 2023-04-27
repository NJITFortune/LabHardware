#!/usr/bin/python

# Import libraries
import RPi.GPIO as GPIO
import time
import datetime
from time import sleep

# Pinouts from RPi Zero 2 W
# 22 Panel on		24 LepiLED on
# 27 Panel off		23 LepiLED off

# Set up pin for latching relay FOR THE LepiLED ON
GPIO.setmode(GPIO.BCM)
# Latching Relay #1
GPIO.setup(24, GPIO.OUT)

# Pin 24 turns LepiLED on
GPIO.output(24, 1)
sleep(0.1)
GPIO.output(24, 0)

# Reset the pin
GPIO.cleanup(24)

# Make an entry in the logfile
nowdate = datetime.datetime.now()
nowsec = round(time.time())

outfile = open("/home/arducam/rpi1.csv", "a")
curtim = nowdate.strftime("RPi1, LepiLED_On, %a %d %b %H:%M:%S %Y, ") 
newlin = " \n"
outfile.write(curtim + str(nowsec) + newlin)
outfile.close()

