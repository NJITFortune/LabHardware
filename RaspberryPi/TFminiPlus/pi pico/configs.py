import board
import busio

# Loop time
LOOP_SLEEP_TIME_INTERVAL = 0.01  # Time interval between each cycle of writing data - adjust for your needs (now is set to ~100 writes per sec)

# TFMini configs
TFMINI_TIMEOUT = 1  # how long we'll wait for valid data or response, in seconds. Default is 1 - response time depends on the sensor's output data rate
TFMINI_RX_PIN = board.GP1  # if necessary change to the proper GPIOs - GP1?
TFMINI_TX_PIN = board.GP0  # if necessary change to the proper GPIOs - GP0?
TFMINI_FRAME_RATE = 300 # in Hz

# SD card configs
BATCH_SIZE = 5000 # How many data lines to write to SD card at a time
SD_SPI = board.SPI()  # Create SPI connection on default pins
# If needed you can set custom pins
# SD_SPI = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
#SD_CS = board.GP9



# enable/disable debug mode
DEBUG = True