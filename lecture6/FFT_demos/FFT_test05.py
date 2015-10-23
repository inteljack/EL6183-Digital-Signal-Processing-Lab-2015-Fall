# FFT_test05.py

# Real FFT

import numpy as np
from matplotlib import pyplot as plt

N = 20
n = np.linspace(0, N-1, N)  # N points from 0 to N-1 inclusive
x = np.cos(2.5 * 2.0 * np.pi / N * n)
X = np.fft.rfft(x)
g = np.fft.irfft(X)
print len(x),type(x)
print len(X)
print len(g)
err = x - g                 # reconstruction error

print 'max(abs(err)) = ', np.max(np.abs(err))

fig = plt.figure(1)

plt.subplot(2, 1, 1)
plt.stem(n, x)
plt.xlim(-1, N)
plt.title('Signal')

k = range(len(X))

plt.subplot(2, 1, 2)
plt.stem(k, abs(X))
plt.xlim(-1, N)
plt.title('Spectrum')

fig.savefig('FFT_test05.pdf')
plt.show()


