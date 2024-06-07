import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import ADS1263
import RPi.GPIO as GPIO
import time

REF = 5.08  # Modify according to actual voltage
            # external AVDD and AVSS(Default), or internal 2.5V
duration_seconds = 10
interval_ms = 10  # Update interval in milliseconds
channelList = [0]  # The channel must be less than 10

# Initialize the ADC
ADC = ADS1263.ADS1263()

# The faster the rate, the worse the stability
# and the need to choose a suitable digital filter(REG_MODE1)
if (ADC.ADS1263_init_ADC1('ADS1263_4800SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0)  # 0 is singleChannel, 1 is diffChannel

# Set up the plot
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'b-', animated=True)

def init():
    ax.set_xlim(0, duration_seconds)
    ax.set_ylim(-REF, REF)
    return ln,

def update(frame):
    ADC_Value = ADC.ADS1263_GetAll(channelList)  # Get ADC1 value
    fooval = REF * 2 - ADC_Value[0] * REF / 0x80000000
    xdata.append(time.time() - start_time)
    ydata.append(fooval)
    xdata = xdata[-1000:]  # Keep only the last 1000 samples for rolling display
    ydata = ydata[-1000:]
    ax.set_xlim(xdata[0], xdata[-1])
    ln.set_data(xdata, ydata)
    return ln,

start_time = time.time()
ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, duration_seconds, duration_seconds*100), 
                              init_func=init, blit=True, interval=interval_ms)

plt.show()

# Clean up
ADC.ADS1263_Exit()
GPIO.cleanup()

