#/bin/sh

# Ensure that the folders have been made
~/bin/MKDirs.sh

# Ensure that the panel lights are on for the photos
~/bin/PaneLightsOn.py

# Take the photos for each camera
i2cset -y 10 0x24 0x24 0x02
	cd ~/Pictures/Camera0a
	~/bin/autoFocus.sh
	sleep 1
	cd ~/Pictures/Camera0m
	~/bin/manualFocus.sh
	sleep 1

i2cset -y 10 0x24 0x24 0x12
	cd ~/Pictures/Camera1a
	~/bin/autoFocus.sh
	sleep 1
	cd ~/Pictures/Camera1m
	~/bin/manualFocus.sh
	sleep 1

i2cset -y 10 0x24 0x24 0x22
	cd ~/Pictures/Camera2a
	~/bin/autoFocus.sh
	sleep 1
	cd ~/Pictures/Camera2m
	~/bin/manualFocus.sh
	sleep 1

i2cset -y 10 0x24 0x24 0x32
	cd ~/Pictures/Camera3a
	~/bin/autoFocus.sh
	sleep 1
	cd ~/Pictures/Camera3m
	~/bin/manualFocus.sh
	sleep 1

echo "RPi1, Cameras, `date`, `date +%s`" >> ~/rpi1.csv

