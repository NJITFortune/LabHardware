#/bin/sh

# Ensure that the folders have been made
~/bin/MKDirs.sh

# Ensure that the panel lights are on for the photos
~/bin/PaneLightsOn.py

echo "RPi7, Cameras start, `date`, `date +%s`" >> ~/rpi7.csv

## Take the photos for each camera

# Camera 0
sudo i2cset -y 10 0x24 0x24 0x02
	sleep 1
	cd ~/Pictures/Camera0a
timeout 20 libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1
	cd ~/Pictures/Camera0m
timeout 20 libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1

# Camera 1
sudo i2cset -y 10 0x24 0x24 0x12
	sleep 1
	cd ~/Pictures/Camera1a
timeout 20 libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1
	cd ~/Pictures/Camera1m
timeout 20 libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1

# Camera 2
sudo i2cset -y 10 0x24 0x24 0x22
	sleep 1
	cd ~/Pictures/Camera2a
timeout 20 libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1
	cd ~/Pictures/Camera2m
timeout 20 libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1

# Camera 3
sudo i2cset -y 10 0x24 0x24 0x32
	sleep 1
	cd ~/Pictures/Camera3a
timeout 20 libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1
	cd ~/Pictures/Camera3m
timeout 20 libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1

echo "RPi7, Cameras stop, `date`, `date +%s`" >> ~/rpi7.csv

# Turn the panel lights back off 
~/bin/PaneLightsOff.py
