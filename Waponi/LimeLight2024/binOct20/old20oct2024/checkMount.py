def is_drive_mounted(device):
    """Check if the specified device is mounted."""
    with open('/proc/mounts', 'r') as mounts:
        for line in mounts:
            if device in line:
                return True
    return False

# Example usage:
device = '/dev/sda'  # Replace with your device path
if is_drive_mounted(device):
    print(f"{device} is mounted.")
else:
    print(f"{device} is not mounted.")

