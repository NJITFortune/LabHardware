# This script uses the GP0 pin to select data logger
# mode (low) or webserver mode (High)
#
import machine

# Check the state of GP0 to determine which function
gp0_state = machine.Pin(0, machine.Pin.IN).value()

# Choose the script to run based on the GP0 state
# UP/HIGH is webserver
# DOWN/LOW is accelerometer data logger

if gp0_state == 1:  # GP0 pulled up
    print("GP0 pulled up. Running the WEBSERVER")
    with open("webserverAP.py", 'rb') as source_file:
        # Read the content of the source file
        content = source_file.read()
    # Open the destination file for writing
    with open("main.py", 'wb') as destination_file:
        # Write the content to the destination file
        destination_file.write(content)

else:  # GP0 pulled down
    print("GP0 pulled down. Running DATA COLLECTION")
    with open("MicroShaker.py", 'rb') as source_file:
        # Read the content of the source file
        content = source_file.read()
    # Open the destination file for writing
    with open("main.py", 'wb') as destination_file:
        # Write the content to the destination file
        destination_file.write(content)

