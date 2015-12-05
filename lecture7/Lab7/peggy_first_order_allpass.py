# first_order_allpass.py
import scipy.io as sio
import scipy
from scipy import signal
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
# import numpy as np

x = sio.loadmat('onetothreeh.mat')
x = x['onetothreeh'] 
x.tolist()
c = 0.9    # c = pole
print x
b = [np.conjugate(c),-1]
a = [-1,c]

y = scipy.signal.lfilter(b, a, x)
w, h = signal.freqz(y)
fig = plt.figure()
plt.title('Digital filter frequency response')
ax1 = fig.add_subplot(111)

plt.plot(w, 20 * np.log10(abs(h)), 'b')
plt.ylabel('Amplitude [dB]', color='b')
plt.xlabel('Frequency [rad/sample]')

ax2 = ax1.twinx()
angles = np.unwrap(np.angle(h))
plt.plot(w, angles, 'g')
plt.ylabel('Angle (radians)', color='g')
plt.grid()
plt.axis('tight')
plt.show()

