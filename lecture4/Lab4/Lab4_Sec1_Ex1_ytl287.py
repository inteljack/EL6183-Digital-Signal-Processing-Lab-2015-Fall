from math import cos 
from math import pi 
import pyaudio
import struct
import wave


output_wavefile = "output.wav"

# 16 bit/sample

# Fs : Sampling frequency (samples/second)
Fs = 8000
# Fs = 16000   
# Fs = 32000

T = 2       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play

# Pole location
f1 = 800
f2 = 400
om1 = 2.0*pi * float(f1)/Fs
om2 = 2.0*pi * float(f2)/Fs

r = 0.999      # Try other values, 0.998, 0.9995, 1.0
r = float(r)    # Ensure r is a float
# Qustion: how to set r to obtain desired time constant?

# Difference equation coefficients
l_a1 = -2*r*cos(om1)
r_a1 = -2*r*cos(om2)
l_a2 = r_a2 = r**2

print 'l_a1 = ', l_a1
print 'l_a2 = ', l_a2

# Initialization
y1 = 0.0
y2 = 0.0
y11 = 0.0
y12 = 0.0
gain = 10000.0

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,  
                channels = 2, 
                rate = Fs,
                input = False, 
                output = True, 
                frames_per_buffer = 1)

output_wf = wave.open(output_wavefile, 'w')      # wave file
output_wf.setframerate(Fs)
output_wf.setsampwidth(2)
output_wf.setnchannels(2)

for n in range(0, N):

    # Use impulse as input signal
    if n == 0:
        x0 = 1.0
    else:
        x0 = 0.0

    # Difference equation
    y0 = x0 - l_a1 * y1 - l_a2 * y2

    # Delays
    y2 = y1
    y1 = y0

    # Difference equation
    y10 = x0 - r_a1 * y11 - r_a2 * y12

    # Delays
    y12 = y11
    y11 = y10

    # Output
    l_out = gain * y0
    r_out = gain * y10
    str_out = struct.pack('hh', l_out,r_out)     # 'h' for 16 bits
    stream.write(str_out, 1)
    output_wf.writeframes(str_out)

print("* done *")

stream.stop_stream()
stream.close()
p.terminate()
