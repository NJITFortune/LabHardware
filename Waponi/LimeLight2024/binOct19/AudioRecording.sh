#!/bin/sh

arecord -D hw:CARD=Microphone,DEV=0 -f S16_LE -r 384000 -d 30 /home/arducam/foobar.wav
