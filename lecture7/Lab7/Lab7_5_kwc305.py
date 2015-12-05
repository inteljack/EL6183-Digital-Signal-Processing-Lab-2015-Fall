
import pyaudio
import struct
import wave
import math
import numpy as np
from matplotlib import pyplot as plt
import myfunctions
import  scipy.signal as signal
# import scipy.io as sio

RATE = 10000

a = np.array([5.0, -4.0, 3.0,-2.0,1.0])
# a = np.array([1.0,-2.0,3.0, -4.0, 5.0])
# a = [5,-4,3,-2,1]
b = list(a)
divider = a[0]

b.reverse()

a = map(lambda x: x/divider,a)
b = map(lambda x: x/divider,b)

print 'a=',a
print 'b=',b

# compute the frequency response
w, h = signal.freqz(b,a,RATE)
plt.xlabel('Normalized Frequency-notch 1(n)')
plt.ylabel('dB')
plt.ylim(-5, 5)        # set y-axis limits
plt.xlim(0, 5) 
plt.plot(w, (h))


plt.show()

print '* Done'
















