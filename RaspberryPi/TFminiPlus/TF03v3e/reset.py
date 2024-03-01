from serial import Serial
import time

TTF03_UART_PORT = '/dev/serial0'
TTF03_TIMEOUT = 1

available_baud_rates = [
    115200, 1000000, 9600, 14400, 19200, 38400, 56000, 57600, 128000, 230400,
    256000, 460800, 512000, 750000, 921600, 1500000, 2000000
]

for baud_rate in available_baud_rates:
    print(baud_rate)
    uart = Serial(port=TTF03_UART_PORT, baudrate=baud_rate, timeout=TTF03_TIMEOUT)
    # send reset command
    uart.write(bytearray(b'\x5A\x04\x10\x6E'))
    time.sleep(0.1)
    while True:
        counter = uart.in_waiting
        #print(f'in wait: {counter}')
        if counter > 4:
            recv = uart.read(9)
            uart.reset_input_buffer()
            if recv:
                print(recv)
                if recv == bytearray(b'\x5A\x05\x10\x00\x6F'):
                    print("command sent correctly")
                else:
                    print("wrong response")
                break

    #save the data
    uart.write(bytearray(b'\x5A\x04\x11\x6F'))
    time.sleep(0.1)
    while True:
        counter = uart.in_waiting
        #print(f'in wait: {counter}')
        if counter > 4:
            recv = uart.read(9)
            uart.reset_input_buffer()
            if recv:
                print(recv)
                if recv == bytearray(b'\x5A\x05\x11\x00\x70'):
                    print("command sent correctly")
                else:
                    print("wrong response")
                break


    time.sleep(2)
    uart.close()
