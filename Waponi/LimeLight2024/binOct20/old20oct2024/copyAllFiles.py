#!/usr/bin/python

import shutil
import os

def copy_directory_contents(source_dir, dest_dir):
    """Copies all the contents of source_dir, including subdirectories, to dest_dir."""
    
    # Check if the source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory {source_dir} does not exist.")
        return
    
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Copy all the contents of the source directory to the destination
    for item in os.listdir(source_dir):
        src_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isdir(src_path):
            # Recursively copy directories
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        else:
            # Copy individual files
            shutil.copy2(src_path, dest_path)
    
    print(f"Contents of {source_dir} are ready to be copied to {dest_dir}.")

# Example usage
source_directory = '/home/arducam/data'
destination_directory = '/mnt/usb'

copy_directory_contents(source_directory, destination_directory)
print(f"Syncing data to USB.")
os.sync()
print(f"Sync COMPLETE!")
