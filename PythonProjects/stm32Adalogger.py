import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import storage
import sdioio  # SDIO interface for faster SD card writes
import neopixel
import gc  # Garbage collection

# SD Card Setup
sd = sdioio.SDCard(slot=sdioio.SDCard.SLOT_4)
vfs = storage.VfsFat(sd)
storage.mount(vfs, "/sd")

# I2C and ADS1015 Setup
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)
ads.data_rate = 3300  # Max sample rate (~3.3 kHz)
adc = AnalogIn(ads, ADS.P0)

# NeoPixel Setup
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.2

# Constants
SAMPLES_PER_FILE = 30000
FILE_INDEX = 0

def get_new_filename():
    return f"/sd/log_{FILE_INDEX:03d}.csv"

def blink_blue():
    """Blink onboard NeoPixel blue at ~20 Hz for 1 second."""
    for _ in range(20):
        pixel.fill((0, 0, 255))  # Blue
        time.sleep(0.025)
        pixel.fill((0, 0, 0))  # Off
        time.sleep(0.025)

# Start Logging
FILE_INDEX = 0
while True:
    file_path = get_new_filename()
    
    with open(file_path, "w") as file:
        file.write("Timestamp_10us,ADC_Value\n")  # CSV Header
        print(f"Logging to {file_path}...")

        start_time = time.monotonic_ns() // 10000  # Convert to 10 µs units
        
        for i in range(SAMPLES_PER_FILE):
            timestamp = (time.monotonic_ns() // 10000) - start_time
            adc_value = max(0, min(65535, adc.value))  # Clamp ADC value
            
            file.write(f"{timestamp},{adc_value}\n")
            
            if i % 100 == 0:
                file.flush()  # Flush to SD card every 100 writes

            if i % 1000 == 0:
                gc.collect()  # Run garbage collection to free memory

    print(f"File saved: {file_path}")
    
    # Blink NeoPixel between files
    blink_blue()

    FILE_INDEX += 1  # Move to next file

