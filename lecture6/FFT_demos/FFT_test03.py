# FFT_test03.py

import numpy as np

N = 10
n = np.linspace(0, N-1, N)  # N points from 0 to N-1 inclusive
x = np.cos(2.0 * np.pi / N * n)
X = np.fft.fft(x)
g = np.fft.ifft(X)
err = x - g                 # reconstruction error

print 'n = ', n
print 'x = ', x
print 'X = ', X
print 'max(abs(err)) = ', np.max(np.abs(err))

