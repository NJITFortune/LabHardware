#!/bin/sh
# This is a simple script to run SUDO to mount the portable drive.
# An appropriate fstab entry is required. Here is an example:
# /dev/sda /mnt/usb vfat defaults,noauto,uid=1000,gid=1000,dmask=000,fmask=111 0 0

mount /mnt/usb
