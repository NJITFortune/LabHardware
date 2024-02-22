#/bin/sh

# Ensure that the folders have been made
~/bin/MKDirs.sh

# Ensure that the panel lights are on for the photos
~/bin/PaneLightsOn.py
sleep 10

echo "RPi9, Camera start, `date`, `date +%s`" >> ~/rpi9.csv

# Take the photos for each camera
/usr/sbin/i2cset -y 10 0x24 0x24 0x02
	sleep 1
	cd ~/Pictures/Camera0a
timeout 20 libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
	# ~/bin/autoFocus.sh
	sleep 1
	cd ~/Pictures/Camera0m
	# ~/bin/manualFocus.sh
timeout 20 libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1

/usr/sbin/i2cset -y 10 0x24 0x24 0x12
	sleep 1
	cd ~/Pictures/Camera1a
	# ~/bin/autoFocus.sh
timeout 20 libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1
	cd ~/Pictures/Camera1m
	# ~/bin/manualFocus.sh
timeout 20 libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1

/usr/sbin/i2cset -y 10 0x24 0x24 0x22
	sleep 1
	cd ~/Pictures/Camera2a
	# ~/bin/autoFocus.sh
timeout 20 libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1
	cd ~/Pictures/Camera2m
	# ~/bin/manualFocus.sh
timeout 20 libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1

/usr/sbin/i2cset -y 10 0x24 0x24 0x32
	sleep 1
	cd ~/Pictures/Camera3a
	# ~/bin/autoFocus.sh
timeout 20 libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1
	cd ~/Pictures/Camera3m
	# ~/bin/manualFocus.sh
timeout 20 libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1

echo "RPi9, Camera stop, `date`, `date +%s`" >> ~/rpi9.csv

# libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
# libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99
