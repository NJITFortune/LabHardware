#!/usr/bin/python
#
# This script checks the status of Button 23 (testButton.py).
# If pulled up (open), collect Audioe, Studio, and GPS data.
# If pulled down (closed), a user is at the device to download.
# Check to see if download process is started, if not, run it.
#
# For the future, there should be only one status checking code.
# This code is identical to dataStudio.py, dataAudioStudioGPS.py
# Also relies on takeStudioPhoto.sh, usbFileManagement.py

import time
import subprocess
import shutil
import os

#### Definitions

# Define paths
datadir = '/home/arducam/data'  # Modify this if your directory is different
studioPhoto = '/home/arducam/bin/takeStudioPhoto.sh'  # Path to photo script
audioSample = '/home/arducam/bin/takeAudioSample.sh'  # Path to audio script
getGPS = '/home/arducam/bin/getGPS.sh' # Path to GPS logger
file2CheckPathName = '/home/arducam/FileCopyInitiated.txt' # We use this file 

#### Code

# Check to see the status of the copy-to-usb process
def check_file_exists():
    return os.path.exists(file2CheckPathName)

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
        subprocess.run([studioPhoto], check=True)
        print(f"Script {studioPhoto} executed successfully.")
    except subprocess.CalledProcessError as es:
        print(f"Error running script: {es}")

    try:
        subprocess.run([audioSample], check=True)
        print(f"Script {audioSample} executed successfully.")
    except subprocess.CalledProcessError as ea:
        print(f"Error running script: {ea}")

if openORclosed.returncode == 0:
    print(f"Button is closed, do not read GPS, take photo, nor audio")
    if check_file_exists():
        print(f'{file2CheckPathName} exists, copying already in process.')
    else:
        print(f'{file2CheckPathName} does not exist, start copying process.')
        subprocess.Popen(['python3', '/home/arducam/bin/usbFileManagement.py'])

