#!/home/arducam/plotter/bin/python

import pandas as pd
import matplotlib.pyplot as plt
import sys

## User option
if len(sys.argv) == 1:   # The only argument is the script name
    skipsam = 2
else:			 # We have an argument, which is the number of samples to skip
    skipsam = int(sys.argv[1])

## Read values from CSV file
data = pd.read_csv('data.csv') # Read data from CSV file
yval = data['adc_value']       # Read the amplitude data from the CSV file
xtim = data['timestamp_ns']    # Read the timestamp data from the CSV file

## Adjust time values
xtim = xtim - xtim[1]	       # Start time at zero instead of relative to 1970
xtim = xtim / 1000000000       # Convert from nanoseconds to seconds   
length = len(xtim)             # How many samples do we have?

## Plot
fig, ax1 = plt.subplots(1, 1)  # Create a single panel figure

# Uncomment one of the three options below for look
ax1.plot(xtim[0:length:skipsam], yval[0:length:skipsam])
# ax1.plot(xtim[0:length:skipsam], yval[0:length:skipsam], marker = ".")
# ax1.plot(xtim, yval)

# plt.tight_layout()

ax1.set_title('ADC Test')

plt.savefig('xyz.png')

## SETING UP THE VIRTUAL ENVIRONMENT
# python3 -m venv ~/plotter
# plotter/bin/pip3 install pandas
# plotter/bin/pip3 install matplotlib
