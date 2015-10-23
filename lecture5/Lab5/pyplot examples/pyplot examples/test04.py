
from matplotlib import pyplot as plt

plt.figure(1)

plt.xlim(0, 20)
plt.ylim(0, 10)

line1, = plt.plot([], [])   # Create empty line

# plt.setp(line1, xdata = [1, 17, 9, 11], ydata = [1, 9, 4, 8])
# OR
line1.set_data( [1, 17, 9, 11], [1, 9, 4, 8])

plt.setp(line1, color = 'r', linewidth = 2)

line1.set_xdata( [ 1, 3, 5, 7] )

plt.show()




