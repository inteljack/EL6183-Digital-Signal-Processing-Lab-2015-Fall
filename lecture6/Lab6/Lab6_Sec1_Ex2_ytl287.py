# plot_micinput_spectrum.py

"""
Using Pyaudio, get audio input and plot real-time FFT of blocks.
Ivan Selesnick, October 2015
Based on program by Gerald Schuller
"""

import pyaudio
import struct
import numpy as np
from matplotlib import pyplot as plt
from math import log10
import os
import sys
file_name =  os.path.basename(sys.argv[0])
filename = file_name[:-3] + '_capture.pdf'

plt.ion()           # Turn on interactive mode so plot gets updated

WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
RATE = 16000      	# Sampling rate (samples/second)
BLOCKSIZE = 512
DURATION = 10       # Duration in seconds

NumBlocks = int( DURATION * RATE / BLOCKSIZE )
print 'NumBlocks =', NumBlocks
print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks
print 'Running for ', DURATION, 'seconds...'
# print_block = input('Which block would you like to save as a pdf file?:')
print_block = 100

# Initialize plot window:
plt.figure(1)
plt.ylim(0, 50*log10(10*RATE))
plt.ylabel('dB')

# plt.xlim(0, BLOCKSIZE/2.0)         # set x-axis limits
# plt.xlabel('Frequency (k)')
# f = np.linspace(0, BLOCKSIZE-1, BLOCKSIZE)

# # Time axis in units of milliseconds:
plt.xlim(0, 1000*log10(RATE/2.0))         # set x-axis limits
plt.xlabel('Frequency (Hz) in 10^3*log10')
plt.xlabel('Frequency (Hz)')
f = [n*float(RATE/BLOCKSIZE) for n in range(BLOCKSIZE)]
# f[0] = 0.000000001
# for j in range(0, len(f)):
# 	f[j] = 1000*log10(f[j])
# print len(f)
line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(f)                         # x-data of plot (frequency)

# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = False)
for i in range(0, NumBlocks):
    input_string = stream.read(BLOCKSIZE)                     # Read audio input stream
    input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)  # Convert
    X = np.fft.fft(input_tuple)
    X = abs(X)
    listX = X.tolist()

    for j in range(0, len(listX)):
    	if listX[j] == 0:
    		listX[j] = 0.00000000001
    	listX[j] = 20 * log10(listX[j])
    line.set_ydata(listX)                               # Update y-data of plot
    plt.draw()
    
    if i == print_block:
		plt.figure(1).savefig(filename)
		print "save a capture"

# plt.close()
# print np.shape(listX)
stream.stop_stream()
stream.close()
p.terminate()

print '* Done'
