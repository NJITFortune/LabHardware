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
    TF03_FRAME_RATE,
    TTF03_TIMEOUT,
    TTF03_UART_PORT,
    NO_OF_READINGS,
)

distance = 0
strength = 0
value_counter = 0

def ifprint(txt: str):
    if DEBUG:
        print(txt)

def create_filename(path:str = os.getcwd()):
    return f'/{len([i for i in os.listdir(path) if ".csv" in i])}.csv'

async def uart_client():
    global distance, strength
    uart = Serial(port=TTF03_UART_PORT,baudrate=1000000,timeout=TTF03_TIMEOUT)
    time.sleep(0.01)
    
    print("Starting Sampling")
    value_counter = 0
    while (value_counter < NO_OF_READINGS):
        counter = uart.in_waiting
        #print(f'in wait: {counter}')
        if counter >8:
            recv = uart.read(9)
            uart.reset_input_buffer()
            if recv:
                # print(recv)
                if recv[0] == 0x59 and recv[1] == 0x59: 
                    distance = recv[2] + recv[3] * 256
                    strength = recv[4] + recv[5] * 256
                    ifprint(f'({distance},{strength})')
                    value_counter += 1
        await asyncio.sleep(0)
    print(f'{NO_OF_READINGS} samples recorded. Stopping logging.')

async def log():
    global distance, strength
    print('Creating logger')
    logger = Logger(batch_size=BATCH_SIZE,headers= "timestamp,distance,strength",file_name=create_filename(), path=os.getcwd())  # creating logger with appropriate headers
    while True:
        loop_time = time.monotonic_ns()
        # print(f'{loop_time},{distance},{strength}')
        logger.log_data(f'{loop_time},{distance},{strength}')
        await asyncio.sleep(LOOP_SLEEP_TIME_INTERVAL)

async def main():
    clients = [asyncio.create_task(uart_client())]
    clients.append(asyncio.create_task(log()))
    await asyncio.gather(*clients)

loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()
