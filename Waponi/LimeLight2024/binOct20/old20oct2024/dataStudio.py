#!/usr/bin/python
# This script checks that the button is in the correct position and
# runs the data aquisition. Button 23 must be open.
# This is the "bottom of the minute" script that only captures photos.

import time
import subprocess
import shutil
import os
import sys

#### Definitions

# Define paths
datadir = '/home/arducam/data'  # Modify this if your directory is different
studioPhoto = '/home/arducam/bin/takeStudioPhoto.sh'  # Path to photo script
file2CheckPathName = '/home/arducam/FileCopyInitiated.txt'

def check_file_exists():
    return os.path.exists(file2CheckPathName)

# Read GPIO Pin 23
openORclosed = subprocess.run(['python3', '/home/arducam/bin/testButton.py'], capture_output=True, text=True)

# When the pin is pulled up (released), run the shell script(s)
if openORclosed.returncode == 1:
    print(f"Button is high, time to collect only Studio data bottom of the minute")

    try:
        subprocess.run([studioPhoto], check=True)
        print(f"Script {studioPhoto} executed successfully.")
    except subprocess.CalledProcessError as es:
        print(f"Error running script: {es}")

if openORclosed.returncode == 0:
    print(f"Button is grounded, do not take photo")
    if check_file_exists():
        print(f'{file2CheckPathName} exists, copying already in process.')
    else:
        print(f'{file2CheckPathName} does not exist, start copying process.')
        subprocess.Popen(['python3', '/home/arducam/bin/usbFileManagement.py'])

