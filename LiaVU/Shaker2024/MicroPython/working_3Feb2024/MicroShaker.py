# DataLogger for Shaking Stick Syndrome
# February 2024, NJIT BIOL150 Living in a Variable Universe
# Logs 2500 samples at approximately 250 Hz sample rate
# Saves to CSV, sequentially in data#.csv where # is 0-7
#
import machine
import utime
import MPU6050
import uos
import sys

# This allows us to control the Pico W LED
led = machine.Pin("LED", machine.Pin.OUT)

# Set up the I2C interface for the Accelerometer
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
# Set up the MPU6050 class
mpu = MPU6050.MPU6050(i2c)

# This function counts the number of csv files in the root directory
def countCSVfiles():
    filelist = uos.listdir("/")
    csv_files = [file for file in filelist if file.endswith(".csv")]
    return len(csv_files)

# Get the number of CSV files in the root directory
# If there are more than 8 files, our Pico will be full - so let the user know
numCSVfiles = countCSVfiles()

if numCSVfiles > 8:
    print('Too many files on device')
    for _ in range(100):
        led.on()
        utime.sleep_ms(50)
        led.off()
        utime.sleep_ms(100)
    sys.exit()
else:
    filename = "data{}.csv".format(numCSVfiles + 1)

# wake up the MPU6050 from sleep
mpu.wake()

print('Blink startup sequence')
for _ in range(2):
    led.on()
    utime.sleep_ms(1000)
    led.off()
    utime.sleep_ms(1000)
for _ in range(2):
    led.on()
    utime.sleep_ms(500)
    led.off()
    utime.sleep_ms(500)

# LED is on during the sample period
led.on()

# Open the data file for append and write header
d = open(filename, "a")
d.write("T, X, Y, Z \n")
runtime = 0

print("Starting data collection... \n")
# Collect the acceleration data
numCycles = 2500
while numCycles > 0:
#    d.write("%i" % utime.time_ns() + ", %.2f, %.2f, %.2f \n" % (mpu.readacceldata()))
    d.write("%i" % utime.ticks_ms() + ",\t %.2f,\t %.2f,\t %.2f \n" % (mpu.readacceldata()))
    utime.sleep_ms(2)
    numCycles = numCycles - 1

print("Data collection complete. \n")
led.off()
utime.sleep_ms(500)
print("Last gasp... \n")
led.on()
utime.sleep_ms(500)
led.off()

d.flush()
d.close()
