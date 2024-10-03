#!/bin/sh

head -20 /dev/ttyAMA0 | strings | grep RMC | tail -1 >> /home/arducam/data/gpsData.csv

