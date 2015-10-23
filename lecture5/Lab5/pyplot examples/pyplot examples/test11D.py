# subplots

from matplotlib import pyplot as plt
import numpy as np

x = np.linspace(0, 5, 20)
y = x ** 2

ax1 = plt.subplot(2, 1, 1)
line1, = plt.plot(x, y, 'red')
plt.title('x^2')

ax2 = plt.subplot(2, 1, 2)
line2, = plt.plot( y, x,  'blue')
ax2.set_title('x^0.5')

plt.setp(ax1, title = 'new title')

plt.show()

