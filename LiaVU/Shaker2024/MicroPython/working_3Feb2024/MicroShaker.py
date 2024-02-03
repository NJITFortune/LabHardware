# Write your code here :-)
import machine
import utime
import MPU6050
import uos

# Set up the I2C interface
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
# Set up the MPU6050 class
mpu = MPU6050.MPU6050(i2c)

# This function counts the number of csv files in the root directory
def count_csv_files():
    file_list = uos.listdir("/")
    csv_files = [file for file in file_list if file.endswith(".csv")]
    return len(csv_files)

# Get the number of CSV files in the root directory
num_csv_files = count_csv_files()
filename = "data{}.csv".format(num_csv_files)

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
d = open(filename, "a")
d.write("T, X, Y, Z \n")
runtime = 0

print("Starting data collection... \n")
# Collect the acceleration data
numCycles = 2500
while numCycles > 0:
    d.write("%i" % utime.time_ns() + ", %.2f, %.2f, %.2f \n" % (mpu.readacceldata()))
    utime.sleep_ms(2)
    numCycles = numCycles - 1

print("Data collection complete. \n")
led.off()
d.flush()
d.close()
