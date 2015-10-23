# FFT_test02.py

import numpy as np

x = np.array([0, 1, 2, 3, 4])
X = np.fft.fft(x)
g = np.fft.ifft(X)
err = x - g

print 'x is a', type(x)
print 'X is a', type(X)
print 'g is a', type(g)
print 'err is a', type(err)

print 'x = ', x
print 'X = ', X
print 'max(err) = ', max(err)
