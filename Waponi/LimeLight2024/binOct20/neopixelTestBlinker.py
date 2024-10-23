#!/home/arducam/neopixel/bin/python3
#
# requires adafruit-circuitpython-neopixel-spi
# Setup in virtual environment
# python3 -m venv neopixel
# cd neopixel
# bin/pip3 install adafruit-circuitpython-neopixel-spi

# Import libraries
import time
import board
import neopixel_spi 

# RPi version in 2024 needs SPI.  Hopefully this will be fixed soon.
pixels = neopixel_spi.NeoPixel_SPI(board.SPI(), 10)
print(f'NeoPixel is set')

print(f'Displaying red blinks')
# Display red and blink at 2 Hz for 10 seconds
count = 0
while count < 3:
    pixels.fill(0xff0000)
    pixels.fill(0xff0000)
    time.sleep(0.5)
    pixels.fill(0x000000)
    pixels.fill(0x000000)
    time.sleep(0.5)
    count += 1

time.sleep(0.1)

print(f'Displaying green blinks')
count = 0
while count < 6:
    pixels.fill(0x008000)
    pixels.fill(0x008000)
    time.sleep(0.25)
    pixels.fill(0x000000)
    pixels.fill(0x000000)
    time.sleep(0.25)
    count += 1

time.sleep(0.1)

print(f'Displaying blue blinks')
count = 0
while count < 30:
    pixels.fill(0x0000FF)
    pixels.fill(0x0000FF)
    time.sleep(0.05)
    pixels.fill(0x000000)
    pixels.fill(0x000000)
    time.sleep(0.05)
    count += 1

# Ensure that the LED is off
pixels.fill(0x000000)
pixels.fill(0x000000)

