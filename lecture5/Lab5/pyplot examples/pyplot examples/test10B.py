# Inset axis

from matplotlib import pyplot as plt
import numpy as np

x = np.linspace(0, 5, 10)
y = x ** 2

fig1 = plt.figure(1)

ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
ax2 = fig1.add_axes([0.2, 0.5, 0.4, 0.3]) # inset axes

# main figure
ax1.plot(x, y, 'r')
plt.setp(ax1, xlabel = 'x', ylabel = 'y', title = 'title')

# insert
ax2.plot(y, x, 'g')
plt.setp(ax2, xlabel = 'x', ylabel = 'y', title = 'inset title')

fig1.savefig('test10B.pdf')

plt.show()

