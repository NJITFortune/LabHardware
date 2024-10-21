#!/usr/bin/python

import shutil
import time
import os
import subprocess

### Custom

import config as c

# Define source and destination paths
usb_device = c.usb_dev
datadir = c.data_path  # Modify this if your directory is different
usbdrive = c.usb_path  # Update this to match your USB mount point

# Helper programs
sudoMount = c.mountusb
sudoUmount = c.umountusb
statusLED = c.statusLED
checkUSBcopy = c.checkUSBcopy

file2CheckPathName = c.file2CheckPathName

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

################### Check if USB has sufficient space
def is_enough_space():
    """Check if USB has sufficient space."""
    enoughSpace = subprocess.run([checkUSBcopy])
    if enoughSpace.returncode == 0:
        return True
    if enoughSpace.returncode == 1:
        return False

#################### Mount USB device routine
def sudo_mount():

    try:
        # Run the shell script with sudo
        result = subprocess.run(['sudo', sudoMount], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running the script as sudo: {e}")
        print(f"Script error output: {e.stderr}")

#################### unMount USB device routine
def sudo_umount():

    try:
        # Run the shell script with sudo
        result = subprocess.run(['sudo', sudoUmount], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    except subprocess.CalledProcessError as e:
        print(f"Error running the script as sudo: {e}")
        print(f"Script error output: {e.stderr}")

#################### Copy files to USB
def copy_files_to_usb():
    """Copy files from the curdat directory to the USB drive."""

    ### Make sure that the USB drive is mounted (check and if not, prompt user)
    while not is_drive_mounted(usb_device):
        print(f"Waiting for {usb_device} to be mounted...")
        ledBlink = subprocess.Popen([statusLED, '2'])
        sudo_mount()
        time.sleep(11)  # Wait 11 seconds before checking again

    ### Make sure that there is enough space on USB (check and if not, prompt user to replace)
    if not is_enough_space():
        print(f"Oops - {usb_device} is too full... please replace")
        sudo_umount()
        ledBlink = subprocess.Popen([statusLED, '3'])
        time.sleep(10)
        print(f"Removing tracking file because there was insufficient space.")
        os.remove(file2CheckPathName)
        ledBlink.kill()
        time.sleep(1)
        ledBlink = subprocess.Popen([statusLED, '4'])
        time.sleep(1)
        ledBlink.kill()
        exit(1)

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
    ledBlink = subprocess.Popen([statusLED, '1'])
    os.sync()

    print(f"Copy complete, waiting 5 seconds and unmounting USB drive.")
    time.sleep(5)
    ledBlink.kill()
    sudo_umount()
    time.sleep(1)
    ledBlink = subprocess.Popen([statusLED, '4'])
    time.sleep(1)
    ledBlink.kill()

    print(f"Removing tracking file.")
    os.remove(file2CheckPathName)
    print(f"Done.")

############ Run the script
print(f"Initiating file copy routine.")
copy_files_to_usb()

