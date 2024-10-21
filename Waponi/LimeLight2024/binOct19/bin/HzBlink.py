#!/usr/bin/python

from gpiozero import LED
from time import sleep

# Set up the LED on GPIO 12
led = LED(12)

# Blink the LED at 1Hz (0.5 seconds on, 0.5 seconds off)
for _ in range(10):  # 1Hz for 10 seconds means 10 cycles
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)

