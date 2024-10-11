from gpiozero import Button
from signal import pause
import os
import shutil
import subprocess

# Define paths
datadir = '/home/arducam/curdat'  # Modify this if your directory is different
usbdrive = '/mnt/usb'  # Update this to match your USB mount point
dataq = '/home/arducam/bin/foobar.sh'  # Path to the shell script

# Switch is connected to GPIO pin 23
button = Button(23)

def copy_files_to_usb():
    """Copy files from the curdat directory to the USB drive."""
    if not os.path.exists(usbdrive):
        print("USB drive not found.")
        return

    # Loop through files in the Pictures directory and copy to USB
    for filename in os.listdir(datadir):
        source_file = os.path.join(datadir, filename)
        destination_file = os.path.join(usbdrive, filename)

        try:
            if os.path.isfile(source_file):
                shutil.copy2(source_file, destination_file)  # Copy with metadata
                print(f"Copied {filename} to USB.")
        except Exception as e:
            print(f"Error copying {filename}: {e}")

def run_dataq():
    """Run the shell script when GPIO pin is pulled down."""
    try:
        subprocess.run([dataq], check=True)
        print(f"Script {dataq} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")

# When the pin is pulled up (pressed), copy files to the USB drive
button.when_pressed = copy_files_to_usb

# When the pin is pulled down (released), run the shell script
button.when_released = run_dataq

# Keep the script running to listen for button presses
print("Monitoring GPIO pin 23...")
pause()  # This keeps the program running and waiting for the button to be pressed


