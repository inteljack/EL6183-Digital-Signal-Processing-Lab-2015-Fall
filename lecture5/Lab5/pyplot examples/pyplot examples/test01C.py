
from matplotlib import pyplot as plt

x = [1, 3, 9, 8, 4, 6]
y = [5, 1, 4, 2, 2, 4]
z = [6, 3, 1, 8, 5, 9]

# Two plots with color, short method
plt.figure(1)
plt.plot(x, y, 'red')
plt.plot(y, x, 'blue')
plt.xlabel('Time (n)')

plt.show()

