
# Loop time
LOOP_SLEEP_TIME_INTERVAL = 0.01  # Time interval between each cycle of writing data - adjust for your needs (now is set to ~100 writes per sec)

# TFMini configs
TFMINI_TIMEOUT = 1  # how long we'll wait for valid data or response, in seconds. Default is 1 - response time depends on the sensor's output data rate
TFMINI_FRAME_RATE = 300 # in Hz
TFMINI_UART_PORT = '/dev/ttyAMA0' # change to the appropriate one
# SD card configs
BATCH_SIZE = 5000 # How many data lines to write to SD card at a time
NUM_SAMPLE = 10000

DEBUG = True
