#!/bin/sh
# This is a simple script to capture a Studio Photo. To do this, we cycle
# the attractor and Studio LED lights. GPIO12 is Studio relay, GPIO16 is 
# attractor relay. Photo is captured using libcamera. Photos are named
# using the "datetime" option, and an entry is made in the data log.

# This is our path - set it to match config.py data_path + Studio
DIR="/home/arducam/data/curdat/Studio"

# Check if the directory exists
if [ ! -d "$DIR" ]; then
  # Directory doesn't exist, create it
  echo "Directory $DIR does not exist. Creating it..."
  mkdir -p "$DIR"
fi

cd $DIR

# Turn off attractor and turn on Studio lights

echo "Turning GPIO 12 ON - Studio lights"
gpioset gpiochip0 12=1   # Set GPIO 12 to high (3.3V)

echo "Turning GPIO 16 OFF - attractor"
gpioset gpiochip0 16=0   # Set GPIO 16 to low (0V)

# Sleep 2 seconds to ensure that the lights are stable
sleep 2
# Capture the photo
libcamera-still -n --datetime

# Log the capture
filename=`ls -t *.jpg | head -1`
echo "studio, "$filename", OwlSight, 4624x3472" >> /home/arducam/data/curdat/dataLog.csv

# Sleep 2 second to ensure that everything is completed before switching.

echo "Turning GPIO 16 ON - attractor"
gpioset gpiochip0 16=1   # Set GPIO 16 to high (3.3V)

echo "Turning GPIO 12 OFF - Studio lights"
gpioset gpiochip0 12=0   # Set GPIO 12 to low (0V)

