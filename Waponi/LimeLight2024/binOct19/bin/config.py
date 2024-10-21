#!/usr/bin/python

# Path
base_path = '/home/arducam'
bin_path = '/home/arducam/bin'
data_path = '/home/arducam/data'
backup_path = '/home/arducam/backup'

# Which GPIO pins will we use?
studio_gpio = 12
attractor_gpio = 16
neopixel_gpio = 13

# Which data do we want to collect?
data_studio = 1
data_audio = 1
data_gps = 1
data_environmental = 0

# Interval to collect data (in seconds)?
crontab_interval = 30

