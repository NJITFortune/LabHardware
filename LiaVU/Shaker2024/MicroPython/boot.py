from machine import Pin

# Define the pin that would be checked to see if the program should run.
# In this case it's GP0, connect a button between it and GND.
start = Pin(0, Pin.IN, Pin.PULL_UP)

if start():
	# Change myprogram to whatever you renamed your current main.py to.
	import webrepl
	webrepl.start()
