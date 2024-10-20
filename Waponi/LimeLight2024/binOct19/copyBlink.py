import shutil
import time
from gpiozero import LED
from threading import Thread

# Set up the LED on GPIO12
led = LED(12)

# Function to blink the LED
def blink_led():
    while blinking:
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)

# Function to copy a file
def copy_file(src, dst):
    global blinking
    blinking = True

    # Start the LED blinking in a separate thread
    blink_thread = Thread(target=blink_led)
    blink_thread.start()

    # Copy the file
    shutil.copy(src, dst)

    # Stop the LED from blinking once the copy is done
    blinking = False
    blink_thread.join()  # Ensure the blink thread finishes cleanly

    # Turn off the LED
    led.off()

if __name__ == "__main__":
    # Example usage: copying a file
    source_file = "/path/to/source/file"
    destination_file = "/path/to/destination/file"
    
    copy_file(source_file, destination_file)
    print("File copy complete.")

