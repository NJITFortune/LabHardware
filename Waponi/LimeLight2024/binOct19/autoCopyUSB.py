from gpiozero import Button
import shutil
import time
import os

# GPIO setup
BUTTON_GPIO = 17
button = Button(23)

# Define source and destination paths
SOURCE_DIR = '/home/arducam/testola'
DESTINATION_DIR = '/mnt/usb'  # Update with your USB drive mount point

def copy_data():
    try:
        # Ensure destination directory exists
        if not os.path.exists(DESTINATION_DIR):
            print(f"Destination directory {DESTINATION_DIR} does not exist.")
            return
        
        # Copying files
        print("Copying files...")
        for item in os.listdir(SOURCE_DIR):
            s = os.path.join(SOURCE_DIR, item)
            d = os.path.join(DESTINATION_DIR, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, False, None)
            else:
                shutil.copy2(s, d)
        print("Copy completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

def button_callback(channel):
    print("Button pressed!")
    copy_data()

# Add event detection on the button
button.when_pressed = copy_data

try:
    print("Waiting for button press...")
    while True:
        time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
    print("Exiting...")

