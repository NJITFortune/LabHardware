# Use the ImageHandling environment

import os
import csv
import datetime
import matplotlib.pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS

# Define the start time (modify as needed)
START_TIME = datetime.datetime(2020, 1, 1, 0, 0, 0)

def get_exif_data(image_path):
    """Extracts EXIF data from a given image file."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data is None:
            return None
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == "DateTimeOriginal":
                return value
    except Exception as e:
        print(f"Error reading EXIF data from {image_path}: {e}")
    return None

def convert_to_time_int(exif_time):
    """Converts EXIF timestamp to an integer based on 100 ms resolution."""
    if exif_time is None:
        return None
    dt = datetime.datetime.strptime(exif_time, "%Y:%m:%d %H:%M:%S")
    time_diff = dt - START_TIME
    return int(time_diff.total_seconds())  # 1 s resolution

def process_images(source_directory):
    """Processes JPG images in a directory and saves EXIF timestamps to a CSV file."""
    image_times = []
    csv_filename = os.path.join(source_directory, "image_times.csv")
    
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Filename", "Time"])
        
        for filename in sorted(os.listdir(source_directory)):
            if filename.lower().endswith(".jpg"):
                image_path = os.path.join(source_directory, filename)
                exif_time = get_exif_data(image_path)
                time_int = convert_to_time_int(exif_time)
                if time_int is not None:
                    image_times.append((filename, time_int))
                    writer.writerow([filename, time_int])
    
    return image_times

def plot_time_differences(image_times):
    """Plots the time difference between sequential images."""
    if len(image_times) < 2:
        print("Not enough images to plot time differences.")
        return
    
    times = [t[1] for t in image_times]  # Extract time values

    time_diffs = [t2 - t1 for t1, t2 in zip(times[:-1], times[1:])]  # Compute differences
    inv_time_diffs = [1/d if d != 0 else float('inf') for d in time_diffs]  # Compute 1/diffs

    time_vals = times[1:]  # Align diffs to second timestamp
    
    plt.figure(figsize=(10, 5))
    plt.plot(time_vals, time_diffs, marker='o', linestyle='-', color='b')
    plt.xlabel("Time)")
    plt.ylabel("dTime")
    plt.title("Time Between Sequential Images")
    plt.grid(True)
    plt.show()

def main(source_directory):
    image_times = process_images(source_directory)
    plot_time_differences(image_times)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <source_directory>")
    else:
        main(sys.argv[1])

