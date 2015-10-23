
from matplotlib import pyplot as plt

x = [1, 3, 9, 8, 4, 6]
y = [5, 1, 4, 2, 2, 4]
z = [6, 3, 1, 8, 5, 9]

# Three plots 
plt.figure(1)
plt.plot(x, y, 'r-')
plt.plot(y, x, 'bo-')
plt.plot(x, z, 'gs--')
plt.xlabel('Time (n)')

# Three plots 
plt.figure(2)
plt.plot(x, y, 'r-', linewidth = 2)
plt.plot(y, x, 'bo-', markersize = 5)
plt.plot(x, z, 'gs--', markersize = 10, linewidth = 4)
plt.xlabel('Time (n)')

plt.show()

