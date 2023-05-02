
print('Raspberry pi version')
import time
import os
from lib.sd_logger import Logger
import asyncio
from serial import Serial
from configs import (
    LOOP_SLEEP_TIME_INTERVAL,
    DEBUG,
    BATCH_SIZE,
    TFMINI_FRAME_RATE,
    TFMINI_TIMEOUT,
    TFMINI_UART_PORT,
    NUM_SAMPLES
)

distance:str = 0
strength:str = 0


def setFrameRate(frame_rate:int) ->bytearray:
    cmndData = bytearray(b'\x06\x06\x03\x00\x00\x00\x00\x00')
    cmndLen = cmndData[ 1] #  Save the second byte as command length.
    cmndData[ 0] = 0x5A #  Set the first byte to HEADER code.
    cmndData[3:2] = (frame_rate).to_bytes(2,'little') #  add the 2 byte FrameRate parameter
    cmndData = cmndData[0:cmndLen]  # re-establish command data length
    #  Create a checksum byte for the command data array.
    chkSum = 0
    #  Add together all bytes but the last.
    for i in range( cmndLen -1):
        chkSum += cmndData[ i]
    #  and save it as the last byte of command data.
    cmndData[ cmndLen -1] = ( chkSum & 0xFF)
    return cmndData


def ifprint(txt: str)->None:
    if DEBUG:
        print(txt)

def create_filename(path:str = os.getcwd())->str:
    return f'/{len([i for i in os.listdir(path) if ".csv" in i])}.csv'

async def uart_client():
    global distance, strength
    uart = Serial(port=TFMINI_UART_PORT,baudrate=115200,timeout=TFMINI_TIMEOUT) # Establish UART connection
    print(f"Sending command for setting frame rate to {TFMINI_FRAME_RATE}Hz")
    uart.write(setFrameRate(TFMINI_FRAME_RATE)) # Setting the frame rate
    time.sleep(0.01)
    print("command sent")
    while True:
        counter = uart.in_waiting # checking for waiting bytes 
        if counter >8: # if there are 9 or more bytes in waiting 
            recv = uart.read(9) # Get a read
            uart.reset_input_buffer() # reset the input buffer
            if recv: # if there is read data
                if recv[0] == 0x59 and recv[1] == 0x59: # Check if the first 2 bytes are 0x59 (valid response from TFmini)
                    # Validate the checksum
                    checksum = 0
                    for i in range(0, 8):
                        checksum = checksum + recv[i]
                    checksum = checksum % 256
                    if checksum == recv[8]: # if checksum is valid
                        distance = recv[2] + recv[3] * 256 # calculate distance(cm)
                        strength = recv[4] + recv[5] * 256 # calculate strength -  When the signal strength is lower than 100 or equal to 65535, the detection is unreliable, TFmini Plus will set distance value to 0.
                        ifprint(f'({distance},{strength},)') # if debug is true - print readings
        await asyncio.sleep(0) # Release the interpreter 


async def log():
    print('Creating logger')
    num_samples=NUM_SAMPLES
    logger = Logger(
        batch_size=BATCH_SIZE,
        headers= "timestamp,distance,strength",
        file_name=create_filename(),
        path=os.path.join(os.getcwd(),'data')
        )
    sample_count = 0  # initialize the sample count
    while sample_count < num_samples:  # continue logging data until the desired number of samples have been logged
        loop_time = time.monotonic_ns()
        logger.log_data(f'{loop_time},{distance},{strength}')
        sample_count += 1  # increment the sample count
        await asyncio.sleep(LOOP_SLEEP_TIME_INTERVAL)
    print(f'{num_samples} samples recorded. Stopping logging.')
    

async def main():
    print('TFmini-plus data logger')
    clients = [asyncio.create_task(uart_client())]
    clients.append(asyncio.create_task(log()))
    await asyncio.gather(*clients)

loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()
