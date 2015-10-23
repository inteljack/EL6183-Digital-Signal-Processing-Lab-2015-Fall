
from matplotlib import pyplot as plt

x = [1, 3, 9, 8, 4, 6]
y = [5, 1, 4, 2, 2, 4]

plt.figure(1)

lines = plt.plot( x, y, y, x )   # 'lines' is a tuple

plt.xlabel('Time (n)')

# For line properties you can set: plt.setp(lines)

lines[0].set_label('apples')
lines[1].set_label('bananas')

lines[0].set_linewidth(5)
lines[1].set_linewidth(3)

plt.legend()

plt.show()

