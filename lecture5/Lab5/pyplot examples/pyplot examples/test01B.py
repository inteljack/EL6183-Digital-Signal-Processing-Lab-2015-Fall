
from matplotlib import pyplot as plt

x = [1, 3, 9, 8, 4, 6]
y = [5, 1, 4, 2, 2, 4]
z = [6, 3, 1, 8, 5, 9]

# One plot
plt.figure(1)
plt.plot(x, y)
plt.xlabel('Time (n)')
plt.ylabel('Amplitude')
plt.title('Data')

# Two plots with color
plt.figure(2)
plt.plot(x, y, color = 'red')
plt.plot(y, x, color = 'blue')
plt.xlabel('Time (n)')

plt.show()

