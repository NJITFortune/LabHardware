# Import Libraries
import time
import busio
import board
import adafruit_mpu6050
# Note that storage is imported in boot.py

# Initialize the I2C Connection
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
mpu = adafruit_mpu6050.MPU6050(i2c)

# Open the data file for append and write header
data = open("log.csv", "a")
data.write("X, Y, Z \n")
runtime = 0

# Collect the acceleration data
numCycles = 2000
sleepTime = 0.005
while runtime <= numCycles:
    tmpdata = ("%.2f, %.2f, %.2f" % (mpu.acceleration))
    data.write(str(tmpdata) + "\n")
    time.sleep(sleepTime)
    runtime = runtime + 1

data.flush()
data.close()
