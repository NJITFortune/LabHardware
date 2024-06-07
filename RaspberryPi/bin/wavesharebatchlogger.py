#!/usr/bin/python
# -*- coding:utf-8 -*-

import csv
import time
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

# Initialize the ADC
ADC = ADS1263.ADS1263()

# The faster the rate, the worse the stability
# and the need to choose a suitable digital filter(REG_MODE1)
if (ADC.ADS1263_init_ADC1('ADS1263_4800SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0)  # 0 is singleChannel, 1 is diffChannel

# Prepare for CSV writing
with open(file_name, 'w', newline='') as csvfile:
    fieldnames = ['timestamp_ns', 'adc_value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Collect data in a list for batching
    data_batch = []

    while time.time() < end_time:
        ADC_Value = ADC.ADS1263_GetAll(channelList)  # Get ADC1 value
        fooval = REF * 2 - ADC_Value[0] * REF / 0x80000000
        timestamp_ns = time.time_ns()
        data_batch.append({'timestamp_ns': timestamp_ns, 'adc_value': fooval})

        # Write to CSV in batches
        if len(data_batch) >= batch_size:
            writer.writerows(data_batch)
            data_batch = []

        # time.sleep(interval_seconds)

    # Write any remaining data
    if data_batch:
        writer.writerows(data_batch)

# Clean up
ADC.ADS1263_Exit()
GPIO.cleanup()

