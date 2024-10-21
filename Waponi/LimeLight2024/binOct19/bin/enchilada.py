import time
import subprocess
from gpiozero import Button
import shutil
import os
from signal import pause

#### Definitions

# Define the USB device and shell script path
usb_device = '/dev/sda'  # Replace with your device path

# Define paths
datadir = '/home/arducam/curdat'  # Modify this if your directory is different
usbdrive = '/mnt/usb'  # Update this to match your USB mount point
dataq = '/home/arducam/bin/foobaroo.sh'  # Path to the shell script

# Switch is connected to GPIO pin 23
button = Button(23)

#### Copy files to USB
def copy_files_to_usb():
    """Copy files from the curdat directory to the USB drive."""

    while not is_drive_mounted(usb_device):
        sudo_mount()
        time.sleep(1)  # Wait 1 second before checking again
        print(f"Waiting for {usb_device} to be mounted...")

    # Loop through files in the Pictures directory and copy to USB
    print(f"Device {usb_device} is mounted, copying files")
    for filename in os.listdir(datadir):
        source_file = os.path.join(datadir, filename)
        destination_file = os.path.join(usbdrive, filename)

        try:
            if os.path.isfile(source_file):
                shutil.copy2(source_file, destination_file)  # Copy with metadata
                print(f"Copied {filename} to USB.")
        except Exception as e:
            print(f"Error copying {filename}: {e}")

    print(f"Copy complete!")
    time.sleep(5)
    sudo_umount()

#### Check if USB is mounted
def is_drive_mounted(device):
    """Check if the specified device is mounted."""
    with open('/proc/mounts', 'r') as mounts:
        for line in mounts:
            if device in line:
                return True
    return False

#### Mount USB device
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

#### unMount USB device
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

def run_dataq():
    """Run the shell script when GPIO pin is pulled down."""
    try:
        subprocess.run([dataq], check=True)
        print(f"Script {dataq} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")


# When the pin is pulled down (pressed), copy files to the USB drive
if button.is_pressed:
    print(f"Button closed")
    copy_files_to_usb()

# When the pin is pulled up (released), run the shell script
if not button.is_pressed:
    print(f"Button open")
    run_dataq()

# Keep the script running to listen for button presses
# print("Monitoring GPIO pin 23...")
# pause()  # This keeps the program running and waiting for the button to be pressed

