# Lab7_2_ytl287.py
"""
Using Pyaudio, record sound from the audio device and plot,
for 8 seconds, and display it live in a Window.
Usage example: python pyrecplotanimation.py
Gerald Schuller, October 2014 
Modified: Ying-Ta Lin, October 2015
"""

import pyaudio
import struct
import wave
import math
import cmath
import numpy as np
# from matplotlib import pyplot as plt
from myfunctions import clip16
import sys    
import os

file_name =  os.path.basename(sys.argv[0])

# Open wave file (mono)
wave_file_name = 'sin_440Hz_stereo.wav'
# wave_file_name = 'sin01_mono.wav'
# wave_file_name = 'sin01_stereo.wav'
wf = wave.open( wave_file_name, 'rb')
RATE = wf.getframerate()
WIDTH = wf.getsampwidth()
LEN = wf.getnframes() 
CHANNELS = wf.getnchannels() 
print 'Rate =', RATE
print 'Width =', WIDTH
print 'Number of frames =', LEN
print 'Number of channels =', CHANNELS

def shift(l, n):
    return l[n:] + l[:n]

# plt.ion()           # Turn on interactive mode so plot gets updated

# WIDTH = 2           # bytes per sample
# CHANNELS = 1        # mono
# RATE = 16000        # Sampling rate (samples/second)
# DURATION = 10       # Duration in seconds
BLOCKSIZE = 2**12
f1 = 440
f2 = 500
f3 = 600
alpha1 = 0.4
alpha2 = 0.4
alpha3 = 0.4

# Number of blocks in wave file
NumBlocks = int(math.floor(LEN/BLOCKSIZE))
# NumBlocks = int( DURATION * RATE / BLOCKSIZE )

print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks
# print 'Running for ', DURATION, 'seconds...'

# Initialize plot window:
# plt.figure(1)
# plt.ylim(-10000, 10000)        # set y-axis limits

# plt.xlim(0, BLOCKSIZE)         # set x-axis limits
# plt.xlabel('Time (n)')

t = range(0, BLOCKSIZE)
# a_lpf = np.array([1, -1.2762, 2.6471, -2.2785, 2.1026, -1.1252, 0.4876, -0.1136])
# b_lpf = np.array([0.0423, 0.1193, 0.2395, 0.3208, 0.3208, 0.2395, 0.1193, 0.0423])
# filter_order = 7    # 7 order filter
filter_order = 6


#
cosw1 = math.cos( 2 * math.pi * float(f1) / RATE)
a_apf1 = [1.0+alpha1, -2.0*cosw1, 1.0-alpha1]
b_apf1 = list(a_apf1)
divider1 = a_apf1[0]

b_apf1.reverse()

a_apf1 = map(lambda x: x/divider1,a_apf1)
b_apf1 = map(lambda x: x/divider1,b_apf1)

# 
cosw2 = math.cos( 2 * math.pi * float(f2) / RATE)
a_apf2 = [1.0+alpha2, -2.0*cosw2, 1.0-alpha2]
b_apf2 = list(a_apf2)
divider2 = a_apf2[0]

b_apf2.reverse()

a_apf2 = map(lambda x: x/divider2,a_apf2)
b_apf2 = map(lambda x: x/divider2,b_apf2)

#
cosw3 = math.cos( 2 * math.pi * float(f3) / RATE)
a_apf3 = [1.0+alpha3, -2.0*cosw3, 1.0-alpha3]
b_apf3 = list(a_apf3)
divider3 = a_apf3[0]

b_apf3.reverse()

a_apf3 = map(lambda x: x/divider3,a_apf3)
b_apf3 = map(lambda x: x/divider3,b_apf3)

a = np.convolve(a_apf1,a_apf2)
a = np.convolve(a,a_apf3)
b = np.convolve(b_apf1,b_apf2)
b = np.convolve(b,b_apf3)

# I = cmath.sqrt(-1)
# s = np.array([cmath.exp( I * 0.5 * np.pi * K) for K in range(0,filter_order+1)])

print a
print b
# # Time axis in units of milliseconds:
# plt.xlim(0, 1000.0*BLOCKSIZE/RATE)         # set x-axis limits
# plt.xlabel('Time (msec)')
# t = [n*1000/float(RATE) for n in range(BLOCKSIZE)]

# line, = plt.plot([], [], color = 'blue')  # Create empty line
# line.set_xdata(t)                         # x-data of plot (time)

# Create block (initialize to zero)
output_block = [0 for n in range(0, BLOCKSIZE)]
Y = [ 0.0 for i in range(0, filter_order+1) ] 
X = [ 0.0 for i in range(0, filter_order+1) ] 
# output signal in all (string)
output_all = ''    

# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True)

# Initialize angle
# theta = 0.0

# Block-to-block angle increment
# theta_del = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi

for i in range(0, NumBlocks):
    input_string = wf.readframes(BLOCKSIZE)                     # Read audio input stream
    input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)    # Convert

    # Go through block
    for n in range(0, BLOCKSIZE):
        # Amplitude modulation  (f0 Hz cosine)
        # output_block[n] = input_tuple[n] * math.cos(2*math.pi*n*f0/RATE + theta)
        # output_block[n] = input_tuple[n] * 1.0  # for no processing
        
        # Difference equation
        X[6] = input_tuple[n]
        Yvalue = a[1] * Y[5] + a[2] * Y[4] + a[3] * Y[3] + a[4] * Y[2] + a[5] * Y[1] + a[6] * Y[0]
        Y[6] = b[0] * X[6] + b[1] * X[5] + b[2] * X[4] + b[3] * X[3] + b[4] * X[2] + b[5] * X[1] + b[6] * X[0] - Yvalue

        # unclipped_value = np.real(Y[7] * cmath.exp(I * 2 *math.pi*n*f0/RATE))
        # output_block[n] = clip16(unclipped_value)
        output_block[n] = clip16(Y[6])
        Y = shift(Y,1)
        X = shift(X,1)
    # Set angle for next block
    # theta = theta + theta_del

    # line.set_ydata(output_block)                               # Update y-data of plot
    # plt.draw()

    # Convert values to binary string
    output_string = struct.pack('h' * BLOCKSIZE, *output_block)

    # Write binary string to audio output stream
    stream.write(output_string)

    # append new to total
    output_all = output_all + output_string
# plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print '* Done'

output_wavefile = file_name[:-3] + '_complex_AM.wav'
print 'Writing to wave file', output_wavefile
wf = wave.open(output_wavefile, 'w')      # wave file
wf.setnchannels(CHANNELS)      # one channel (mono)
wf.setsampwidth(2)      # two bytes per sample
wf.setframerate(RATE)   # samples per second
wf.writeframes(output_all)
wf.close()
print('* Done')