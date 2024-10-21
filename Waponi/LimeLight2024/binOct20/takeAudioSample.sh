#!/bin/sh
# This script takes an Audio Recording from a AudioMoth USB microphone.
# It also makes an entry into our logging file.
# The -d is duration in seconds. We default 30 seconds.

# This is our path - set it to match config.py data_path + Audio
DIR="/home/arducam/data/curdat/Audio"

# Check if the directory exists
if [ ! -d "$DIR" ]; then
  # Directory doesn't exist, create it
  echo "Directory $DIR does not exist. Creating it..."
  mkdir -p "$DIR"
fi

# Set path to match config.py data_path + Audio

timestamp=$(date +"%Y%m%d%H%M%S")
filename="${timestamp}.wav"
arecord -D hw:CARD=Microphone,DEV=0 -f S16_LE -r 384000 -d 30 /home/arducam/data/curdat/Audio/$filename
echo "audio, "$filename", AudioMoth, S16_LE, 384000, 30" >> /home/arducam/data/curdat/dataLog.csv
