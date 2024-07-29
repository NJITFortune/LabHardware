import cv2
import numpy as np
import os

def calculate_luminance(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Calculate average luminance
    luminance = np.mean(gray_image)
    return luminance

def adjust_luminance(image, target_luminance):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Calculate current luminance
    current_luminance = np.mean(gray_image)
    # Calculate the ratio to adjust luminance
    ratio = target_luminance / current_luminance
    # Adjust the image luminance
    adjusted_image = cv2.convertScaleAbs(image, alpha=ratio, beta=0)
    return adjusted_image

def match_luminance_to_reference(ref_image_path, input_dir, output_dir):
    # Read the reference image
    ref_image = cv2.imread(ref_image_path)
    if ref_image is None:
        print(f"Failed to read reference image: {ref_image_path}")
        return
    
    # Calculate the luminance of the reference image
    target_luminance = calculate_luminance(ref_image)
    print(f"Target luminance: {target_luminance}")

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
        adjusted_image = adjust_luminance(image, target_luminance)
        
        # Save the adjusted image
        cv2.imwrite(output_path, adjusted_image)
        print(f"Processed and saved: {output_path}")

if __name__ == "__main__":
    ref_image_path = '/Users/efortune/Downloads/316.png'
#    input_dir = '/Users/efortune/Downloads/lr2024'
#    output_dir = '/Users/efortune/Downloads/lr2024/new'
    input_dir = '/Volumes/SabrentLime/LimelightStudio2024RawImages/Raft5'
    output_dir = '/Volumes/SabrentLime/LimelightStudio2024RawImages/Raft5/0000_new'

    
    match_luminance_to_reference(ref_image_path, input_dir, output_dir)

