#!/usr/bin/python

from gpiozero import LED
from time import sleep

# Set up the LED on GPIO 12
led = LED(12)

# Blink the LED at 0.5Hz (1 second on, 1 second off)
for _ in range(5):  # 0.5Hz for 10 seconds means 5 cycles
    led.on()
    sleep(1)
    led.off()
    sleep(1)

