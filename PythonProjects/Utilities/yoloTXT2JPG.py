# This is a handy-dandy utility to take the txt files that are outputs of yolov8
# for each image file and make a quick CSV file out of it.
# Eric Fortune, 2025, Canopy Life

import os
import pandas as pd
import argparse

# Get user arguments from command line
parser = argparse.ArgumentParser(description="Convert YOLO label TXT files to CSV.")
parser.add_argument("labels_dir", help="Path to the directory containing YOLO label TXT files.")
parser.add_argument("output_csv", nargs="?", default="detections.csv", help="Output CSV file name (default: detections.csv)")
args = parser.parse_args()

labels_dir = args.labels_dir
output_csv = args.output_csv

# Check if the labels directory exists
if not os.path.isdir(labels_dir):
    print(f"Error: Directory '{labels_dir}' not found.")
    exit(1)

# Empty variable - we will append data here for our csv file
data = []

# Loop through all .txt files in the labels directory
for filename in os.listdir(labels_dir):
    if filename.endswith(".txt"):  # Process only TXT files
        filepath = os.path.join(labels_dir, filename)

        # Read the label file and take only the first (category) or last (confidence) columns.
        with open(filepath, "r") as file:
            for line in file:
                values = line.strip().split()
                if len(values) >= 2:  # Ensure valid data
                    category = values[0]  # First column: Category (0, 1, or 2)
                    confidence = values[-1]  # Last column: Confidence

                    # Replace .TXT with .JPG in the filename (May need to change for capitalization)
                    image_filename = filename.replace(".txt", ".JPG")

                    # Append data to list
                    data.append([image_filename, category, confidence])

# Convert to DataFrame and save as CSV
df = pd.DataFrame(data, columns=["filename", "category", "confidence"])
df.to_csv(output_csv, index=False)

print(f"Detections saved to {output_csv}")

