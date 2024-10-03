#!/usr/bin/python
# This script checks that the button is in the correct position and
# runs the data aquisition. Button 23 must be open.
# This is the "daytime" script that runs Audio and GPS.

import time
import subprocess
import shutil
import os

#### Definitions

# Define paths
datadir = '/home/arducam/data'  # Modify this if your directory is different
audioSample = '/home/arducam/bin/takeAudioSample.sh'  # Path to audio script
getGPS = '/home/arducam/bin/getGPS.sh' # Path to GPS logger

# Switch is connected to GPIO pin 23
openORclosed = subprocess.run(['python3', '/home/arducam/bin/testButton.py'], capture_output=True, text=True)

# When the pin is pulled up (released), run the shell script(s)
if openORclosed.returncode == 1:
    print(f"Button open, time to collect data top-of-the-minute")

    try:
        subprocess.run([getGPS], check=True)
        print(f"Script {getGPS} executed successfully.")
    except subprocess.CalledProcessError as eg:
        print(f"Error running script: {eg}")
    print(f"Button open, time to collect data top-of-the-minute")

    try:
        subprocess.run([audioSample], check=True)
        print(f"Script {audioSample} executed successfully.")
    except subprocess.CalledProcessError as ea:
        print(f"Error running script: {ea}")

if openORclosed.returncode == 0:
    print(f"Button is closed, do not read GPS, record audio")
