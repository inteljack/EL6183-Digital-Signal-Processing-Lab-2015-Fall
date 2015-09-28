from math import cos 
from math import pi 
import pyaudio
import struct
import check_samples

# 16 bit/sample

# Fs : Sampling frequency (samples/second)
Fs = 8000
# Fs = 16000   
# Fs = 32000

T = 2       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play

Ta = 0.4           # duration between 0.1-1.0 (decay) [time till 1% amplitude]
Tb = 0.9           # duration (decay) [which over is larger]
r1 = 0.01 ** (1/(Ta*Fs))
r2 = 0.01 ** (1/(Tb*Fs))

# Pole location
f1 = 400
om1 = 2.0*pi * float(f1)/Fs
#r1 = 0.999      # Try other values, 0.998, 0.9995, 1.0
r1 = float(r1)    # Ensure r is a float
# Qustion: how to set r to obtain desired time constant?

# Pole location (second filter)
f2 = 400
om2 = 2.0*pi * float(f2)/Fs
#r2 = 0.999      # Try other values, 0.998, 0.9995, 1.0
r2 = float(r2)    # Ensure r is a float

# Difference equation coefficients
a11 = -2*r1*cos(om1)
a12 = r1**2
a21 = -2*r2*cos(om2)
a22 = r2**2

print 'a11 = ', a11
print 'a12 = ', a12
print 'a21 = ', a21
print 'a22 = ', a22

# Initialization
y11 = 0.0
y12 = 0.0
y21 = 0.0
y22 = 0.0
gain = 1.0

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,  
                channels = 1, 
                rate = Fs,
                input = False, 
                output = True, 
                frames_per_buffer = 1)

for n in range(0, N):

    # Use impulse as input signal
    if n == 0:
        x0 = 1.0
    else:
        x0 = 0.0

    # Difference equation
    y10 = x0 - a11 * y11 - a12 * y12

    # Delays
    y12 = y11
    y11 = y10

    # Difference equation second time
    y20 = y10 - a21 * y21 - a22 * y22

    # Delays
    y22 = y21
    y21 = y20

    # Output
    y20 = check_samples.check(y20,gain)
    out = gain * y20
    str_out = struct.pack('h', out)     # 'h' for 16 bits
    stream.write(str_out, 1)

print("* done *")

stream.stop_stream()
stream.close()
p.terminate()
