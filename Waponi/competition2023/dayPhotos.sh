#/bin/sh

# Ensure that the folders have been made
/home/arducam/bin/MKDirs.sh

# Ensure that the LED lights are off!!!
/home/arducam/bin/PaneLightsOff.py
sleep 1
/home/arducam/bin/LepiLEDoff.py
sleep 1

echo "RPi6, Camera daystart, `date`, `date +%s`" >> /home/arducam/rpi6.csv

# Take the photos for each camera

# CAMERA 0
sudo /usr/sbin/i2cset -y 10 0x24 0x24 0x02
	sleep 1
	cd /home/arducam/Pictures/Camera0a
timeout 20 libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1
	cd /home/arducam/Pictures/Camera0m
timeout 20 libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1

# CAMERA 1
sudo /usr/sbin/i2cset -y 10 0x24 0x24 0x12
	sleep 1
	cd /home/arducam/Pictures/Camera1a
timeout 20 libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1
	cd /home/arducam/Pictures/Camera1m
timeout 20 libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1

# CAMERA 2 
sudo /usr/sbin/i2cset -y 10 0x24 0x24 0x22
	sleep 1
	cd /home/arducam/Pictures/Camera2a
timeout 20 libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1
	cd /home/arducam/Pictures/Camera2m
timeout 20 libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1

# CAMERA 3
sudo /usr/sbin/i2cset -y 10 0x24 0x24 0x32
	sleep 1
	cd /home/arducam/Pictures/Camera3a
timeout 20 libcamera-still -n --autofocus-mode=auto --autofocus-range=macro --sharpness=2 --datetime --exposure=sport --quality=99
	sleep 1
	cd /home/arducam/Pictures/Camera3m
timeout 20 libcamera-still -n --autofocus-mode=manual --lens-position=10 --sharpness=2 --datetime --exposure=sport --quality=99

sleep 1

echo "RPi6, Camera daystop, `date`, `date +%s`" >> /home/arducam/rpi6.csv

