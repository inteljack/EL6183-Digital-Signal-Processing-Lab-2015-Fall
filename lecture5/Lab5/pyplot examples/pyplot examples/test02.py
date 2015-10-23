# import matplotlib
# matplotlib.use('TKAgg')

from matplotlib import pyplot as plt

x = [1, 3, 9, 8, 4, 6]
y = [5, 1, 4, 2, 2, 4]

fig1 = plt.figure(1)
plt.plot( x, y, label = 'apples', linewidth = 2 )
plt.plot( y, x, 'y', label = 'bananas', linewidth = 4 )
plt.xlabel('Time (n)')
plt.legend()
plt.xlim(0, 12)
plt.ylim(0, 10)
plt.show()

fig1.savefig('test02.pdf')

