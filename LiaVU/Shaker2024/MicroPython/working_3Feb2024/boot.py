import machine

# Define the GPIO pin for GP0
GP0_PIN = 0  # Replace with the actual GPIO pin number
# Define the GPI1 pin for GP1
GP1_PIN = 1  # Replace with the actual GPIO pin number

# Check the state of GP0
gp0_state = machine.Pin(GP0_PIN, machine.Pin.IN).value()
gp1_state = machine.Pin(GP1_PIN, machine.Pin.IN).value()

# Choose the script to run based on the GP0 state
if gp0_state == 1:  # GP0 pulled up
    print("GP0 pulled up. Running the WEBSERVER")
    with open("newwebserverAP.py", 'rb') as source_file:
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

if gp1_state == 1:  # GP1 pulled up
    import datadeleter
else: # GP1 pulled down
    print('GP1 is down, csv files live another day.')
