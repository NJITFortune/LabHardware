import time
import board
import neopixel

# Configure the NeoPixel strip
num_pixels = 1  # Adjust this to the number of pixels in your strip
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels)

# Function to set the color of the NeoPixels
def set_color(pixels, color):
    for i in range(len(pixels)):
        pixels[i] = color
    pixels.show()

# Rainbow colors
rainbow_colors = [
    (255, 0, 0),   # Red
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (75, 0, 130),  # Indigo
    (148, 0, 211),  # Violet
]

# Cycle through colors over 10 seconds
def cycle_colors(pixels, colors, duration):
    start_time = time.monotonic()
    end_time = start_time + duration
    index = 0
    while time.monotonic() < end_time:
        # Set the current color
        set_color(pixels, colors[index])

        # Move to the next color
        index = (index + 1) % len(colors)

        # Wait for a short duration before changing color
        time.sleep(duration / len(colors) / 10)  # Adjust for smoothness

        set_color(pixels, (0, 0, 0))
        time.sleep(0.1)

# Run the color cycle for 10 seconds
cycle_colors(pixels, rainbow_colors, 30)

# Turn off the pixels after cycling
set_color(pixels, (0, 0, 0))
