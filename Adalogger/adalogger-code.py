import os
import busio
import digitalio
import board
import storage
import adafruit_sdcard

import time
import analogio
import struct

# Connect to the card and mount the filesystem.
cs = digitalio.DigitalInOut(board.SD_CS)
sd_spi = busio.SPI(board.SD_CLK, board.SD_MOSI, board.SD_MISO)
sdcard = adafruit_sdcard.SDCard(sd_spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# ADC Setup
adc = analogio.AnalogIn(board.A0)  # Change pin if needed

# Constants
CHUNK_SIZE = 2048  # Buffer size in bytes
MAX_FILE_SIZE = 0.1 * 1024 * 1024  # 20 MB
SAMPLE_RATE_HZ = 4000  # 4 kHz
SAMPLE_PERIOD_US = 250  # 250 µs per sample
FILE_INDEX = 0

# Helper Function to Get New Filename
def get_new_filename():
    global FILE_INDEX
    return f"/sd/log_{FILE_INDEX:03d}.bin"

# Start Logging
buffer = bytearray()
start_time = time.monotonic_ns() // 1000  # Convert to microseconds
FILE_INDEX = 0
file_path = get_new_filename()
file = open(file_path, "wb")

print("Logging started at 4kHz. Writing to:", file_path)

try:
    while True:
        # Wait for the exact sampling interval
        target_time = time.monotonic_ns() // 1000 + SAMPLE_PERIOD_US
        while (time.monotonic_ns() // 1000) < target_time:
            pass  # Busy-wait until the correct sampling time

        # Read ADC and Timestamp
        timestamp = (time.monotonic_ns() // 1000) - start_time  # Microseconds since start
        value = adc.value  # 16-bit ADC reading (0-65535)

        # Pack Data (4-byte timestamp, 2-byte ADC value)
        buffer += struct.pack("<IH", timestamp, value)

        # Flush buffer to SD when reaching CHUNK_SIZE
        if len(buffer) >= CHUNK_SIZE:
            file.write(buffer)
            file.flush()
            buffer = bytearray()

        # Check file size and roll over if needed
        if file.tell() >= MAX_FILE_SIZE:
            file.close()
            FILE_INDEX += 1
            file_path = get_new_filename()
            file = open(file_path, "wb")
            print("New file:", file_path)

except KeyboardInterrupt:
    print("Logging stopped by user.")

except Exception as e:
    print("Error:", e)

finally:
    if buffer:
        file.write(buffer)  # Write any remaining data
    file.close()
    print("File closed. Data saved.")
