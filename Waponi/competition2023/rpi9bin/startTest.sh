#!/bin/sh

# This tests the system

echo "Turn on the LepiLED"
~/bin/LepiLEDon.py

sleep 2 

echo "Turn on the Panel lights"
~/bin/PaneLightsOn.py

sleep 2 

echo "Show all four cameras"
i2cset -y 10 0x24 0x24 0x00
libcamera-still -t 5000

sleep 2 

echo "Turn off Panel lights"
~/bin/PaneLightsOff.py

sleep 2

echo "Turn off LepiKED"
~/bin/LepiLEDoff.py

