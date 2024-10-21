#!/usr/bin/python

from gpiozero import LED
from time import sleep

# Set up the LED on GPIO 12
led = LED(12)

# Blink the LED at 4Hz indefinitely
while True:
    led.on()
    sleep(0.05)  # 20Hz -> 0.025 seconds on
    led.off()
    sleep(0.20)  # 20Hz -> 0.025 seconds off

