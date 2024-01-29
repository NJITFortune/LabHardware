# Import Libraries
import time
import busio
import board
import digitalio
import adafruit_mpu6050
# Note that storage is imported in boot.py

# Initialize the I2C Connection
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
mpu = adafruit_mpu6050.MPU6050(i2c)

# Intialize the LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Open the data file for append and write header
data = open("log.csv", "a")
data.write("T, X, Y, Z \n")
runtime = 0

# Countdown blink, coded the hard (stupid) way
led.value = True
time.sleep(1)
led.value = False
time.sleep(1)
led.value = True
time.sleep(1)
led.value = False
time.sleep(1)
led.value = True
time.sleep(0.5)
led.value = False
time.sleep(0.5)
led.value = True
time.sleep(0.5)
led.value = False
time.sleep(0.5)
led.value = True

# Collect the acceleration data
numCycles = 2000
sleepTime = 0.008
while numCycles > 0:
    tmpdata = ("%.2f, %.2f, %.2f" % (mpu.acceleration))
    data.write(str(time.monotonic_ns()) + str(tmpdata) + "\n")
    time.sleep(sleepTime)
    numCycles = numCycles - 1

led.value = False
data.flush()
data.close()
