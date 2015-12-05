# peggy_two_allpass_notch.py
import scipy.io as sio
import scipy
from scipy import signal
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# import numpy as np

x = sio.loadmat('onetothreeh.mat')
x = x['onetothreeh'] 
x.tolist()
wc1 = 0.3 * np.pi 
alpha1 = 0.02 
b1 = [1+alpha1,-2*np.cos(wc1),1-alpha1]
a1 = [1-alpha1,-2*np.cos(wc1),1+alpha1]
# y1 = scipy.signal.lfilter(b1, a1, x)

wc2 = 0.6 * np.pi 
alpha2 = 0.02 
b2 = [1+alpha2,-2*np.cos(wc2),1-alpha2]
a2 = [1-alpha2,-2*np.cos(wc2),1+alpha2]
# y2 = scipy.signal.lfilter(b2, a2, x)

wc2 = 0.9 * np.pi 
alpha2 = 0.02 
b2 = [1+alpha2,-2*np.cos(wc2),1-alpha2]
a2 = [1-alpha2,-2*np.cos(wc2),1+alpha2]

anew = signal.convolve(a1,a2)
bnew = signal.convolve(b1,b2)

ynew = scipy.signal.lfilter(bnew, anew, x)
w, h = signal.freqz(bnew,anew)
fig = plt.figure()
plt.title('Digital filter frequency response')
ax1 = fig.add_subplot(111)
Id = np.ones(np.size(h))

plt.plot(w, (abs(Id+h)), 'b')
plt.ylabel('Amplitude [dB]', color='b')
plt.xlabel('Frequency [rad/sample]')
ppdf = PdfPages('Lab7_5_phc307_output')
plt.savefig(ppdf,format='pdf')
ppdf.close() 
# ax2 = ax1.twinx()
# angles = np.unwrap(np.angle(h))
# plt.plot(w, angles, 'g')
# plt.ylabel('Angle (radians)', color='g')
plt.grid()
plt.axis('tight')
plt.show()

