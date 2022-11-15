import RPi.GPIO as GPIO
from time import sleep

# Set mode and pin on RPI
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)

# Set the pin to high - 1
GPIO.output(27, 1)

# Wait the desired amount of time
sleep(10)

# Set the pin to low (off) - 0
GPIO.output(27, 0)

# Reset the system to avoid errors
GPIO.cleanup()

