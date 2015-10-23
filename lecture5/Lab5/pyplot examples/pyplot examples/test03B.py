
from matplotlib import pyplot as plt

x = [1, 3, 9, 8, 4, 6]
y = [5, 1, 4, 2, 2, 4]

plt.figure(1)

line, = plt.plot(x, y)   # 'lines' is a tuple
plt.xlabel('Time (n)')

line.set_linewidth(3)
line.set_color('red')

# For other line properties you can set: plt.setp(lines)

plt.show()

