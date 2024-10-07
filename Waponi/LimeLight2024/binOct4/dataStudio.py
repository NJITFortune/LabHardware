#!/usr/bin/python
# 
# This script checks the status of Button 23 (testButton.py).
# If pulled up (open), collect STUDIO photo only.
# If pulled down (closed), a user is at the device to download.
# Check to see if download process is started, if not, run it.
#
# For the future, there should be only one status checking code.
# This code is identical to dataAudioGPS.py, dataAudioStudioGPS.py
# Also relies on takeStudioPhoto.sh, usbFileManagement.py

# IMPORT LIBRARIES
import time
import subprocess
import shutil
import os
import sys

#### Definitions

# Define paths
datadir = '/home/arducam/data'  # Same directory as DUFS Docker server
studioPhoto = '/home/arducam/bin/takeStudioPhoto.sh'  # Photo shell script
file2CheckPathName = '/home/arducam/FileCopyInitiated.txt' # We use this file 


#### Code

# Check to see the status of the copy-to-usb process
def check_file_exists():
    return os.path.exists(file2CheckPathName)

# Read GPIO Pin 23 - the user switch
openORclosed = subprocess.run(['python3', '/home/arducam/bin/testButton.py'], capture_output=True, text=True)

if openORclosed.returncode == 1:

    print(f"Button is high: collecting only Studio photo")
#### Add delete file2CheckPathName
    try:
        subprocess.run([studioPhoto], check=True)
        print(f"Script {studioPhoto} executed successfully.")
    except subprocess.CalledProcessError as es:
        print(f"Error running script: {es}")

if openORclosed.returncode == 0:

    print(f"Button is low, do not take Studio photo")
    if check_file_exists():
        print(f'{file2CheckPathName} exists, copying already in process.')
    else:
        print(f'{file2CheckPathName} does not exist, start copying process.')
        subprocess.Popen(['python3', '/home/arducam/bin/usbFileManagement.py'])

