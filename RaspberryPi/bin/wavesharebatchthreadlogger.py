#!/usr/bin/python
# -*- coding:utf-8 -*-

import csv
import time
import threading
import ADS1263
import RPi.GPIO as GPIO

REF = 5.08  # Modify according to actual voltage
            # external AVDD and AVSS(Default), or internal 2.5V

interval_seconds = 0.00001
duration_seconds = 10
file_name = 'adclog.csv'

start_time = time.time()
end_time = start_time + duration_seconds

channelList = [0]  # The channel must be less than 10
batch_size = 1000  # Number of records to write in one go

data_queue = []
data_lock = threading.Lock()
stop_event = threading.Event()

def write_data_to_csv():
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['timestamp_ns', 'adc_value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        while not stop_event.is_set() or data_queue:
            data_lock.acquire()
            data_to_write = data_queue[:batch_size]
            del data_queue[:batch_size]
            data_lock.release()
            
            if data_to_write:
                writer.writerows(data_to_write)
            time.sleep(0.01)  # Sleep to prevent busy-waiting

# Initialize the ADC
ADC = ADS1263.ADS1263()

# The faster the rate, the worse the stability
# and the need to choose a suitable digital filter(REG_MODE1)
if (ADC.ADS1263_init_ADC1('ADS1263_4800SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0)  # 0 is singleChannel, 1 is diffChannel

# Start the CSV writing thread
csv_thread = threading.Thread(target=write_data_to_csv)
csv_thread.start()

try:
    while time.time() < end_time:
        ADC_Value = ADC.ADS1263_GetAll(channelList)  # Get ADC1 value
        fooval = REF * 2 - ADC_Value[0] * REF / 0x80000000
        timestamp_ns = time.time_ns()

        data_lock.acquire()
        data_queue.append({'timestamp_ns': timestamp_ns, 'adc_value': fooval})
        data_lock.release()

        # time.sleep(interval_seconds)
finally:
    # Signal the CSV writing thread to stop and wait for it to finish
    stop_event.set()
    csv_thread.join()

    # Clean up
    ADC.ADS1263_Exit()
    GPIO.cleanup()

