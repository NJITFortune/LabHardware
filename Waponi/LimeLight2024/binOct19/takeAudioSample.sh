#!/bin/sh
# This script takes an Audio Recording from a AudioMoth USB microphone.
# It also makes an entry into our logging file.
# The -d is duration in seconds. We default 30 seconds.

timestamp=$(date +"%Y%m%d%H%M%S")
filename="${timestamp}.wav"
arecord -D hw:CARD=Microphone,DEV=0 -f S16_LE -r 384000 -d 30 /home/arducam/data/Audio/$filename
echo "audio, "$filename", AudioMoth, S16_LE, 384000, 30" >> /home/arducam/data/dataLog.csv
