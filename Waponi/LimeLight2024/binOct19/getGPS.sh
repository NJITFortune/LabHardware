#!/bin/sh
# This is a trivial GPS reader for RPi5 with Adafruit Ultimate GPS hat. This should
# work with any setup, but may need to change the dev to serial0 or ttyAMA10.
# The 20 lines from the head command is arbitrary - it seems to work well enough.

head -20 /dev/ttyAMA0 | strings | grep RMC | tail -1 >> /home/arducam/data/gpsData.csv

