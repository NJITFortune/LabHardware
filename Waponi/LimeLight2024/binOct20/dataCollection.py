#!/usr/bin/python
#
# This script checks the Mode: 1-collection or 0-download
# If collection, use config.py to collect the appropriate data.
# The code can also accept command line arguments to turn off data collection
# If download, use usbFileManagement.py to download.
#
# Code relies on config.py, which has list of dependent code and paths

import time
import subprocess
import shutil
import os
import sys

### Custom 

import config as c

#### Definitions

# Define paths and scripts
datadir = c.data_path # 
studioPhoto = c.samplePhoto # Path to photo script
audioSample = c.sampleAudio # Path to audio script
getGPS = c.sampleGPS # Path to GPS logger
getEnvironment = c.sampleEnvironment # Path to env logger
file2CheckPathName = c.file2CheckPathName # We use this file to prevent double backup processes
checkMode = c.checkMode
backupProcess = c.fileBackup # 

# What data to collect (user can reject data streams)
takeAudio = c.data_audio
takeEnvironment = c.data_environmental
takeGPS = c.data_gps
takeStudio = c.data_studio

# The user can eliminate one of the data streams - for now this will just be turning off Audio
# In the future, the user can over-ride all of the defaults found in config.py

if len(sys.argv) > 1:
    if sys.argv[1] == "NoAudio":
        takeAudio = 0
    elif sys.argv[1] == "NoStudio":
        takeStudio = 0
    elif sys.argv[1] == "NoGPS":
        takeGPS = 0
    elif sys.argv[1] == "NoEnv":
        takeEnvironment = 0

#### Our code 

# Check to see the status of the copy-to-usb process
def check_file_exists():
    return os.path.exists(file2CheckPathName)

# Check to see which mode: data collection (1) or data download (0)
currentMode = subprocess.run([checkMode], capture_output=True, text=True)

# When the pin is pulled up (released), run the shell script(s)
if currentMode.returncode == 1:
    print(f"DATA COLLECTION MODE")

    if takeGPS == 1:
        try:
            subprocess.run([getGPS], check=True)
            print(f"Script {getGPS} executed successfully.")
        except subprocess.CalledProcessError as eg:
            print(f"Error running script: {eg}")

    if takeStudio == 1:
        try:
            subprocess.run([studioPhoto], check=True)
            print(f"Script {studioPhoto} executed successfully.")
        except subprocess.CalledProcessError as es:
            print(f"Error running script: {es}")

    if takeAudio == 1:
        try:
            subprocess.run([audioSample], check=True)
            print(f"Script {audioSample} executed successfully.")
        except subprocess.CalledProcessError as ea:
            print(f"Error running script: {ea}")

    if takeEnvironment == 1:
        try:
            subprocess.run([getEnvironment], check=True)
            print(f"Script {getEnvironment} executed successfully.")
        except subprocess.CalledProcessError as ea:
            print(f"Error running script: {ea}")

if currentMode.returncode == 0:
    print(f"DATA DOWNLOAD MODE")

    # This code may be called by crontab after the code is already executing - exit cleanly
    if check_file_exists():
        print(f'{file2CheckPathName} exists, copying already in process.')
        exit(0)

    # This is the first time crontab has called the code to initiate backup
    else:
        print(f'{file2CheckPathName} does not exist, start copying process.')
        try:
            subprocess.run([backupProcess], check=True)
            print(f"Script {backupProcess} executed successfully.")
        except subprocess.CalledProcessError as es:
            print(f"Error running script: {es}")
