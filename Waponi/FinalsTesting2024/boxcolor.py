import cv2
import numpy as np
import os

target_color = [255, 255, 0]  # Yellow color
new_color = [0, 255, 0]  # Green color

def adjust_color(image):

    # Create a mask for the target color
    mask = cv2.inRange(image, np.array(target_color), np.array(target_color))
    # Replace the color
    image[mask != 0] = new_color
    newimage = image
    return newimage

def doit(ref_image_path, input_dir, output_dir):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each image in the input directory
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        # Read the input image
        image = cv2.imread(input_path)
        if image is None:
            print(f"Failed to read image: {input_path}")
            continue
        
        # Adjust the image luminance to match the reference
        adjusted_image = adjust_color(image)
        
        # Save the adjusted image
        cv2.imwrite(output_path, adjusted_image)
        print(f"Processed and saved: {output_path}")

if __name__ == "__main__":
    ref_image_path = '/Users/efortune/Downloads/316.png'
#    input_dir = '/Users/efortune/Downloads/lr2024'
#    output_dir = '/Users/efortune/Downloads/lr2024/new'
    input_dir = '/Volumes/SabrentLime/boxes'
    output_dir = '/Volumes/SabrentLime/boxes/0000_color'

    
    doit(ref_image_path, input_dir, output_dir)

