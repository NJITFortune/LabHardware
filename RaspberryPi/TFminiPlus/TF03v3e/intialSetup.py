import time
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

def feedback():
    while True:
        counter = uart.in_waiting
        #print(f'in wait: {counter}')
        if counter >8:
            recv = uart.read(9)
            uart.reset_input_buffer()
            if recv:
                if recv[0] == 0x59 and recv[1] == 0x59: 
                    distance = recv[2] + recv[3] * 256
                    strength = recv[4] + recv[5] * 256
                    ifprint(f'({distance},{strength},)')

def setSaveSettings() -> bytearray:
    # Command to save settings: 5A 04 11 6F
    return bytearray(b'\x5A\x04\x11\x6F')

def rainDisable() -> bytearray:
    # Command to disable rain: 5A 05 64 01 C4
    return bytearray(b'\x5A\x05\x64\x01\xC4')

def changeBaudRate() -> bytearray:
    # Command to change Buad rate to 1 Mbits: 5A 08 06 40 42 0F 00 F9
    return bytearray(b'\x5A\x08\x06\x40\x42\x0F\x00\xF9')

def main():
    print("starting")
    uart = Serial(port=TTF03_UART_PORT,baudrate=115200,timeout=TTF03_TIMEOUT)

    # setting up the Disable rain-fog algorithm
    print("Disable rain function")
    uart.write(rainDisable())
    time.sleep(0.1)
    uart.write(setSaveSettings())
    time.sleep(0.1)

    # set the baud rate
    print("Set baud rate")
    uart.write(changeBaudRate())
    time.sleep(0.1)
    uart.write(setSaveSettings())
    time.sleep(0.1)

    # set the framerate
    print("Set framerate to 5000 Hz")
    uart.write(bytearray(b'\x5A\x06\x03\x88\x13\xFE'))
    time.sleep(0.1)
    uart.write(setSaveSettings())
    time.sleep(0.1)

    while True:
        counter = uart.in_waiting
        if counter > 1:
            recv = uart.read(2)
            uart.reset_input_buffer()
            if recv:
                if recv[0] != 0x59 or recv[1] != 0x59: 
                    print("Settings Done")
                    break


if __name__ == "__main__":
    main()
