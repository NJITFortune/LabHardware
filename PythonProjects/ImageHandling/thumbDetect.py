from ultralytics import YOLO
import cv2

# Load the trained YOLOv5 model
model_path = "best.pt"  # Replace with your trained model path
model = YOLO(model_path)

def detect_thumb(image_path):
    """
    Detects if a human thumb is in the given image.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        bool: True if a thumb is detected, False otherwise.
    """
    # Run YOLOv5 inference
    results = model(image_path)

    # Check for any detections
    for result in results:
        if len(result.boxes) > 0:  # If bounding boxes exist
            return True
    return False

# Example usage
image_file = "test.jpg"  # Replace with your image file path
if detect_thumb(image_file):
    print("Thumb detected!")
else:
    print("No thumb detected.")

