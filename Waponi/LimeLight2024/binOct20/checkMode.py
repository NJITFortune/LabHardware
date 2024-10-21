#!/usr/bin/python

from gpiozero import Button

### Custom
import config as c

# Define button

button = Button(c.switch_gpio)

def is_button_pressed():
    return button.is_pressed

# Print the result
if __name__ == "__main__":
    if is_button_pressed():
        print(f'Button is pressed: 0 Download')
        exit(0)
    else:
        print(f'Button is not pressed: 1 Collect')
        exit(1)
