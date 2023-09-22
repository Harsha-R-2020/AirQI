# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np

# Create sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create and save the plot as an image
plt.figure(figsize=(6, 4))
plt.plot(x, y)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Sample Plot')
plt.grid(True)
plt.savefig('plot.png')
