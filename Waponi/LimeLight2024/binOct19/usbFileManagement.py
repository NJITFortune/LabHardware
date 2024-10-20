#!/usr/bin/python

import shutil
import time
import os
import subprocess

# Define source and destination paths
SOURCE_DIR = '/home/arducam/data'
DESTINATION_DIR = '/mnt/usb'  # Update with your USB drive mount point
usb_device = '/dev/sda'
datadir = '/home/arducam/data'  # Modify this if your directory is different
usbdrive = '/mnt/usb'  # Update this to match your USB mount point

file2CheckPathName = '/home/arducam/FileCopyInitiated.txt'

print(f"Touching control file.")
f = open(file2CheckPathName, 'w')
f.write('File copy process initiated. \n')
f.close()

################### Check if USB is mounted
def is_drive_mounted(device):
    """Check if the specified device is mounted."""
    with open('/proc/mounts', 'r') as mounts:
        for line in mounts:
            if device in line:
                return True
    return False

#################### Mount USB device routine
def sudo_mount():
    # Path to the shell script
    script_path = '/home/arducam/bin/mountUSB.sh'

    try:
        # Run the shell script with sudo
        result = subprocess.run(['sudo', script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Output the result
        print("Script output:")
        print(result.stdout)
    
    except subprocess.CalledProcessError as e:
        print(f"Error running the script as sudo: {e}")
        print(f"Script error output: {e.stderr}")

#################### unMount USB device routine
def sudo_umount():
    # Path to the shell script
    script_path = '/home/arducam/bin/umountUSB.sh'

    try:
        # Run the shell script with sudo
        result = subprocess.run(['sudo', script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Output the result
        print("Script output:")
        print(result.stdout)
   
    except subprocess.CalledProcessError as e:
        print(f"Error running the script as sudo: {e}")
        print(f"Script error output: {e.stderr}")

#################### Copy files to USB
def copy_files_to_usb():
    """Copy files from the curdat directory to the USB drive."""

    while not is_drive_mounted(usb_device):
        sudo_mount()
        processFast = subprocess.Popen(['python3', '/home/arducam/bin/fastBlink.py'])
        time.sleep(11)  # Wait 11 seconds before checking again
        print(f"Waiting for {usb_device} to be mounted...")

    # Loop through files in the source data directory and copy to USB
    print(f"Device {usb_device} is mounted, copying files")
    for filename in os.listdir(datadir):
        source_file = os.path.join(datadir, filename)
        destination_file = os.path.join(usbdrive, filename)

        try:
            if os.path.isfile(source_file):
                shutil.copy2(source_file, destination_file)  # Copy with metadata
                print(f"Copying file {filename} to USB.")
            if os.path.isdir(source_file):
                # Recursively copy directories
                shutil.copytree(source_file, destination_file, dirs_exist_ok=True)
                print(f"Copying directory {filename} to USB.")

        except Exception as e:
            print(f"Error copying {filename}: {e}")
    print(f"Syncing data to USB.")
    fastBlinking = subprocess.Popen(['python3', '/home/arducam/bin/fastBlinking.py'])
    os.sync()
    fastBlinking.kill()
    time.sleep(2)
    forceOff = subprocess.Popen(['python3', '/home/arducam/bin/led12off.py'])
    time.sleep(1)
    forceOff.kill()
    print(f"Copy complete, waiting 5 seconds.")
    processHz = subprocess.Popen(['python3', '/home/arducam/bin/HzBlink.py'])
    time.sleep(5)
    sudo_umount()
    print(f"Removing file.")
    os.remove(file2CheckPathName)
    print(f"Done.")

############ Run the script
print(f"Initiating file copy routine.")
copy_files_to_usb()

