# Write your code here :-)
import machine
import utime
import MPU6050

# Set up the I2C interface
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
# Set up the MPU6050 class
mpu = MPU6050.MPU6050(i2c)

# wake up the MPU6050 from sleep
mpu.wake()

led = machine.Pin("LED", machine.Pin.OUT)

print('Blink Sequence')
led.on()
utime.sleep_ms(1000)
led.off()
utime.sleep_ms(1000)
led.on()
utime.sleep_ms(1000)
led.off()
utime.sleep_ms(1000)
led.on()
utime.sleep_ms(500)
led.off()
utime.sleep_ms(500)
led.on()
utime.sleep_ms(500)
led.off()
utime.sleep_ms(500)
led.on()

# Open the data file for append and write header
d = open("log.csv", "a")
d.write("T, X, Y, Z \n")
runtime = 0

print("Starting data collection... \n")
# Collect the acceleration data
numCycles = 2500
while numCycles > 0:
    d.write("%i" % utime.time_ns() + ", %.2f, %.2f, %.2f \n" % (mpu.read_accel_data()))
    utime.sleep_ms(2)
    numCycles = numCycles - 1

print("Data collection complete. \n")
led.off()
d.flush()
d.close()
