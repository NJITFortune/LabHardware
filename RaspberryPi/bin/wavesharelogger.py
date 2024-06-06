#!/usr/bin/python
# -*- coding:utf-8 -*-

import csv
import time
import ADS1263
import RPi.GPIO as GPIO

REF = 5.08          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V

interval_seconds = 0.00001
duration_seconds = 10
file_name = 'adclog.csv'
start_time = time.time()
end_time = start_time + duration_seconds
channelList = [0]  # The channel must be less than 10

with open(file_name, 'w', newline='') as csvfile:
    fieldnames = ['timestamp_ns', 'adc_value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    ADC = ADS1263.ADS1263()
    
    # The faster the rate, the worse the stability
    # and the need to choose a suitable digital filter(REG_MODE1)
    if (ADC.ADS1263_init_ADC1('ADS1263_4800SPS') == -1):
        exit()
    ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel

    while time.time() < end_time:
        ADC_Value = ADC.ADS1263_GetAll(channelList)    # get ADC1 value
        fooval = REF*2 - ADC_Value[0] * REF / 0x80000000
        timestamp_ns = time.time_ns()        
        writer.writerow({'timestamp_ns': timestamp_ns, 'adc_value':fooval})
        #time.sleep(interval_seconds)

#        for i in channelList:
#            if(ADC_Value[i]>>31 ==1):
#                print("ADC1 IN%d = -%lf" %(i, (REF*2 - ADC_Value[i] * REF / 0x80000000)))  
#            else:
#                print("ADC1 IN%d = %lf" %(i, (ADC_Value[i] * REF / 0x7fffffff)))   # 32bit
#        for i in channelList:
#            print("\33[2A")
        
    ADC.ADS1263_Exit()

ADC.ADS1263_Exit()

exit()

## SETTING UP THE VIRTUAL ENVIRONMENT
# wget https://github.com/joan2937/lg/archive/master.zip
# unzip master.zip
# cd lg-master
# sudo make install
# sudo apt install ttf-wqy-zenhei
# MAYBE NOT sudo apt install python3-rpi-lpgio 
# mkdir -p ~/waveshare/pp
# python3 -m venv waveshare/pp
# waveshare/pp/bin/pip3 install RPi.GPIO
# waveshare/pp/bin/pip3 install spidev
# waveshare/pp/bin/pip3 install numpy
# MAYBE waveshare/pp/bin/pip3 install rpi-lpgio
# cd waveshare
# git clone https://github.com/waveshare/High-Pricision_AD_HAT
# 

