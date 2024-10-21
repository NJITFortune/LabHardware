#!/usr/bin/python

from gpiozero import LED
from time import sleep

# Set up the LED on GPIO 12
led = LED(12)

# Blink the LED at 10Hz (0.05 seconds on, 0.05 seconds off)
for _ in range(100):  # 10Hz for 10 seconds means 100 cycles
    led.on()
    sleep(0.05)
    led.off()
    sleep(0.05)

