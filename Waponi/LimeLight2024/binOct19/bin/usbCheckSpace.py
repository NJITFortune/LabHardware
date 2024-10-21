#!/usr/bin/python

import os
import shutil
import sys

### Get the size of the source directory - this is the data we collected
def get_directory_size(directory):
    """Returns the total size of a directory in bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Add file size
            total_size += os.path.getsize(fp)
    return total_size

### Check to make sure that the USB drive is mounted. This *SHOULD* never fail,
### but this check seems like a wise thing to do given that if the drive isn't 
### mounted, this code incorrectly responds that there is sufficient space for
### the copy, even though there is no drive!
def is_mounted(mount_point):
    """Returns True if the given path is mounted, False otherwise."""
    return os.path.ismount(mount_point)

### This is the code that does the check
def check_space(directory, mount_point):
    """Returns True if directory size is less than available space on the mounted drive."""
    # Check if the mount point is mounted
    if not is_mounted(mount_point):
        print(f"Error: {mount_point} is not mounted.")
        sys.exit(1)

    # Get the size of the directory
    dir_size = get_directory_size(directory)

    # Get the available space on the mount point
    total, used, free = shutil.disk_usage(mount_point)

    # Return True if directory size is less than available space, False otherwise
    return dir_size < free

# Example usage:
directory_path = '/home/arducam/data'
mount_point_path = '/mnt/usb'

if check_space(directory_path, mount_point_path):
    print("There is enough space on the drive.")
else:
    print("Insufficient space on the drive.")
