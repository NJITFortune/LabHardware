#!/usr/bin/python

import pandas as pd
import matplotlib.pyplot as plt

# Read the csv data from a set filename data.csv
data = pd.read_csv('data.csv')

# Set up a figure with 2 plot rows and 1 column
fig, (ax1, ax2) = plt.subplots(2, 1)

# Plot strength to the top plot
ax1.plot(data['timestamp'],data['strength'])
ax1.set_title('Strength')

# Plot distance to the bottom plot
ax2.plot(data['timestamp'],data['distance'])
ax2.set_title('Distance')

# Fix the layout to prevent overlap
plt.tight_layout()

# Save the plot to an image
plt.savefig('xyz.png')

