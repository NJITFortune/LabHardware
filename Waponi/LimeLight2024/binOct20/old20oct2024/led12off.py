#!/usr/bin/python

from gpiozero import LED

# Set up the LED on GPIO 12
led = LED(12)

# Turn off the LED
led.off()

