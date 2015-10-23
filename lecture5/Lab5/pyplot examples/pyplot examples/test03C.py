
from matplotlib import pyplot as plt

x = [1, 3, 9, 8, 4, 6]
y = [5, 1, 4, 2, 2, 4]
z = [6, 3, 1, 8, 5, 9]

plt.figure(1)

line1, = plt.plot(x, y)   # 'lines' is a tuple
plt.xlabel('Time (n)')

plt.setp(line1, linewidth = 3)
plt.setp(line1, color = 'red', linestyle = '--')

line2, = plt.plot(y, x)
plt.setp(line2, linewidth = 2, color = 'blue',
	linestyle = '--', marker = 'o', markersize = 8)


plt.show()

