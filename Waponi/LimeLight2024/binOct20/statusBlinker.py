#!/usr/bin/python

import sys
from gpiozero import LED
from time import sleep

### Custom
import config as c

blinkLED = LED(c.neopixel_gpio)

def blink_PLUGUSB(): # A slower blinking that asks the user to intervene
    while True:
        blinkLED.on()
        sleep(0.05)  # 20Hz -> 0.025 seconds on
        blinkLED.off()
        sleep(0.20)  # 20Hz -> 0.025 seconds off

def blink_COPYING(): # Fast blinking as if machine is working
    while True:
        blinkLED.on()
        sleep(0.05)
        blinkLED.off()
        sleep(0.05)

def blink_REPLACEUSB(): # Double blink that is definitely an error
    while True:
        blinkLED.on()
        sleep(0.2)
        blinkLED.off()
        sleep(0.1)
        blinkLED.on()
        sleep(0.2)
        blinkLED.off()
        sleep(1.6)

def blink_FORCEOFF(): # Ensure that the LED has been turned off
    blinkLED.off()
    sleep(0.1)
    blinkLED.off()

def main():
    # Check if the argument is passed and valid
    if len(sys.argv) != 2 or sys.argv[1] not in ['1', '2', '3', '4', '5']:
        print("Usage: python3 statusBlinker.py <1|5>")
        sys.exit(1)
    
    # Determine the blink frequency based on the argument
    if sys.argv[1] == '1':
        blink_COPYING()
    elif sys.argv[1] == '2':
        blink_PLUGUSB() 
    elif sys.argv[1] == '3':
        blink_REPLACEUSB()
    elif sys.argv[1] == '4':
        blink_FORCEOFF()

if __name__ == "__main__":
    main()

