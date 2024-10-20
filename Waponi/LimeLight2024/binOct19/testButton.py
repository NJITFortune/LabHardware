#!/usr/bin/python
from gpiozero import Button
button = Button(23)

def is_button_pressed():
    return button.is_pressed

# Print the result
if __name__ == "__main__":
    if is_button_pressed():
        exit(0)
    else:
        exit(1)
