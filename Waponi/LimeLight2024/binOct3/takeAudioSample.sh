#!/bin/sh
# This script takes an Audio Recording

timestamp=$(date +"%Y%m%d%H%M%S")
filename="${timestamp}.wav"
arecord -D hw:CARD=Microphone,DEV=0 -f S16_LE -r 384000 -d 30 /home/arducam/data/Audio/$filename
echo "audio, "$filename", AudioMoth, S16_LE, 38400, 30" >> /home/arducam/data/dataLog.csv
