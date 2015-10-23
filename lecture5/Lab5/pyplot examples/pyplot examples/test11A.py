# subplots

from matplotlib import pyplot as plt
import numpy as np

x = np.linspace(0, 5, 20)
y = x ** 2

fig, axes = plt.subplots(nrows = 2, ncols = 2) # returns a tuple
# axes: 2D array

axes[0,0].plot(x, y, 'red')
axes[0,0].set_title('x^2')

axes[0,1].plot(x, x, 'g')
axes[0,1].set_title('x')

axes[1,0].plot( x, x - x**2,  'blue')
axes[1,0].set_title('x - x^2')

axes[1,1].plot( y, x,  'blue')
axes[1,1].set_title('x^0.5')

plt.show()

