
from matplotlib import pyplot as plt
import numpy as np

plt.ion()  # Switch on interactive mode  
# Use plt.ioff() to switch off

for i in range(100):
	x = i/10.0
	plt.plot(x, np.sin(x), 'ro')   # plot each point as a red dot
	plt.draw()                	# Show result

plt.ioff()
plt.show()
