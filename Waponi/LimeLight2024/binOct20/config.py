#!/usr/bin/python

### Paths

backup_path = '/home/arducam/data/backup'
base_path = '/home/arducam'
bin_path = '/home/arducam/bin'
data_path = '/home/arducam/data/curdat'
usb_dev = '/dev/sda'
usb_path = '/mnt/usb'
file2CheckPathName = '/home/arducam/FileCopyInitiated.txt'

### Helper programs

samplePhoto = '/home/arducam/bin/takeStudioPhoto.sh' # Photograph (also controls LEDs)
sampleAudio = '/home/arducam/bin/takeAudioSample.sh' # Audio Sample (ultrasonic microphone)
sampleGPS = '/home/arducam/bin/takeGPS.sh' # Get data from GPS device
sampleEnvironment = '/home/arducam/bin/takeEnvironment.sh' # Get data from environmental sensor package

checkMode = '/home/arducam/bin/checkMode.py' # Decides whether we are in COLLECT (1) or DOWNLOAD (0) mode
checkUSBcopy = '/home/arducam/bin/checkUSBcopySpace.py' # Checks to see if sufficient space to copy to USB
fileBackup = '/home/arducam/bin/usbFileManagement.py' # Copies files to USB and manages internal data

mountusb = '/home/arducam/bin/mountUSB.sh'
umountusb = '/home/arducam/bin/umountUSB.sh'

statusLED = '/home/arducam/bin/statusBlinker.py'

### Which GPIO pins will we use?

attractor_gpio = 16 # LEDs to attract moths
neopixel_gpio = 13 # Indicator LED for user
studio_gpio = 12 # LEDs for photographs
switch_gpio = 23 # User switch for COLLECT or DOWNLOAD modes

### Which data do we want to collect? (1 for yes, 0 for no)

data_audio = 1
data_environmental = 0
data_gps = 1
data_studio = 1

# Interval to collect data (in seconds)?
crontab_interval = 30

