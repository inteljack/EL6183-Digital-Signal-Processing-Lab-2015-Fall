# FFT_test01.py

import numpy as np

x = [0, 1, 2, 3]
X = np.fft.fft(x)
g = np.fft.ifft(X)

print x
print X
print g

print 'x is a', type(x)
print 'X is a', type(X)
print 'g is a', type(g)

