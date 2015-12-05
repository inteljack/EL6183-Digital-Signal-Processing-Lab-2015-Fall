# first_order_allpass.py
import scipy.io as sio
from matplotlib import pyplot as plt
# import numpy as np

x = sio.loadmat('input.mat') # mat format nested ndarray
x = x['x'] #get only the item x because the file has x
x.tolist() # its now a 2 dimension list [1*512]
x = x[0,:]

# print x
a = [5.0,-4.0]
b = list(a)
divider = a[0]

b.reverse()

a = map(lambda x: x/divider,a)
b = map(lambda x: x/divider,b)

print "a =", a
print "b =", b

# # Initialize plot window:
# plt.figure(1)
# plt.ylim(0, 50*log10(10*RATE))
# plt.ylabel('dB')

# Gff = 1

# y[n] = -Gff * x[n] - Gff * y[n-1]
# for n in range(0,len(x)):
# 	y[n] = b[0] * x[n] + b[1] * x[n-1] - a[1] * y[n-1]

