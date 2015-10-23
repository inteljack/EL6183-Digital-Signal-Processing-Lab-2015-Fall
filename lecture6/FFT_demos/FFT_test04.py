# FFT_test04.py

import numpy as np
from matplotlib import pyplot as plt

N = 20
n = np.linspace(0, N-1, N)  # N points from 0 to N-1 inclusive
x = np.cos(2.5 * 2.0 * np.pi / N * n)
X = np.fft.fft(x)

fig = plt.figure(1)

plt.subplot(2, 1, 1)
plt.stem(n, x)
plt.xlim(-1, N)
plt.title('Signal')

plt.subplot(2, 1, 2)
plt.stem(n, abs(X))
plt.xlim(-1, N)
plt.title('Spectrum')

plt.show()
fig.savefig('FFT_test04.pdf')


