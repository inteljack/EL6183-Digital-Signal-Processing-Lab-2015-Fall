# subplots

# import matplotlib
# matplotlib.use('TKAgg')		# optional for mac...

from matplotlib import pyplot as plt
import numpy as np

x = np.linspace(0, 5, 20)
y = x ** 2

fig, axes = plt.subplots(nrows = 1, ncols = 2) # returns a tuple

ax1, ax2 = axes

line1, = ax1.plot(x, y, 'red')
ax1.set_title('x^2')

line2, = ax2.plot( y, x, 'blue')
plt.setp(ax2, title = 'x^0.5')

for ax in axes:
    ax.set_xlabel('x')
    ax.set_ylabel('y')

plt.show()


