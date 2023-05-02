import board
import digitalio
import math
import time
import audiocore
import audiopwmio

# Set up GPIO pin for trigger input
trigger = digitalio.DigitalInOut(board.D2)
trigger.direction = digitalio.Direction.INPUT
trigger.pull = digitalio.Pull.UP

# Set up audio output
audio = audiopwmio.PWMAudioOut(board.A0)
sample_rate = 8000  # 8 kHz sample rate
frequency = 440     # 440 Hz sine wave
duration = 1.0 / frequency  # duration of one cycle of the sine wave

# Generate sine wave samples
samples = []
for i in range(int(duration * sample_rate)):
    sample = int((math.sin(2 * math.pi * frequency * i / sample_rate) + 1) / 2 * 65535)
    samples.append(sample)

# Create audio object with the sine wave samples
wave = audiocore.RawSample(samples)

# Loop forever
while True:
    # Wait for trigger input
    while trigger.value:
        pass
    # Play the sine wave
    audio.play(wave)
    # Wait for the sine wave to finish playing
    while audio.playing:
        pass
