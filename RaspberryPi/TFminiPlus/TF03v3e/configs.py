# Loop time
LOOP_SLEEP_TIME_INTERVAL = 0.00005  # 0.0008 Time interval between each cycle of writing data - adjust for your needs (now is set to ~100 writes per sec)

# TFMini configs
TTF03_TIMEOUT = 1  # how long we'll wait for valid data or response, in seconds. Default is 1 - response time depends on the sensor's output data rate
TF03_FRAME_RATE = 5000 # in Hz
TTF03_UART_PORT = '/dev/serial0' # change to the appropriate one
# SD card configs
BATCH_SIZE = 2000 # How many data lines to write to SD card at a time
NO_OF_READINGS = 20000

DEBUG = False
