#!/bin/bash

# Directory containing images (default: current directory)
IMAGE_DIR="${1:-.}"

# Create an "output" directory if it doesn't exist
OUTPUT_DIR="$IMAGE_DIR/smalls"
mkdir -p "$OUTPUT_DIR"

# Loop through image files
for img in "$IMAGE_DIR"/*.{jpg,JPG,jpeg,png,PNG}; do
    # Check if file exists (in case no matching images)
    [ -f "$img" ] || continue

    # Get filename without path
    filename=$(basename "$img")

    # Resize image to 640px width, keeping aspect ratio
    magick "$img" -resize 640 "$OUTPUT_DIR/$filename"

    echo "Resized: $img -> $OUTPUT_DIR/$filename"
done

echo "All images resized and saved in $OUTPUT_DIR"

