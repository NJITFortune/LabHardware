import cv2
import numpy as np

# Load the image
image = cv2.imread('path_to_your_image.jpg')

# Define the color to be replaced (in BGR format)
target_color = [255, 255, 0]  # Yellow color

# Define the new color (in BGR format)
new_color = [0, 255, 0]  # Green color

# Create a mask for the target color
mask = cv2.inRange(image, np.array(target_color), np.array(target_color))

# Replace the color
image[mask != 0] = new_color

# Save the result
cv2.imwrite('path_to_save_new_image.jpg', image)

# Display the result
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

