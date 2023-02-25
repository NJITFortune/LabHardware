from pwmio import PWMOut
import board
import time
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

rPinky = PWMOut(pin=board.GP3, frequency=250, duty_cycle=0, variable_frequency=False)

while True:
    rPinky.duty_cycle=32768
    led.value = True
    time.sleep(1)
    rPinky.duty_cycle=0
    led.value = False
    time.sleep(1)
