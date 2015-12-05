# Lab6_kwc305
"""
Using Pyaudio, record sound from the audio device and plot,
for 8 seconds, and display it live in a Window.
Usage example: python pyrecplotanimation.py
Gerald Schuller, October 2014 
"""

import pyaudio
import struct
import wave
import math
import cmath
import numpy as np
from matplotlib import pyplot as plt
import myfunctions
import  scipy.signal as signal
# Open wave file (mono)
# wave_file_name = '1500.wav'
wave_file_name = 'chirp.wav'
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

def shift_array(l, n):
    return l[n:] + l[:n]

plt.ion()           # Turn on interactive mode so plot gets updated

BLOCKSIZE = 512
f0 = 0              # 'dock audio'

# Number of blocks in wave file
NumBlocks = int(math.floor(LEN/BLOCKSIZE))
# NumBlocks = int( DURATION * RATE / BLOCKSIZE )

print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks
# print 'Running for ', DURATION, 'seconds...'

# Initialize plot window:
plt.figure(1)
plt.ylim(-100, 180)        # set y-axis limits

plt.xlim(0, RATE/2)         # set x-axis limits
plt.xlabel('Frequency (n)')
plt.ylabel('dB')
# t = range(0, BLOCKSIZE)
t =[n for n in range(0, RATE*2)]

I = cmath.sqrt(-1)
filter_order = 4    # 4 order filter

# a = a_lpf * s
# b = b_lpf * s
# #  notch
# a = np.array([1.0000 ,  -3.9825,    5.9484 ,  -3.9494,    0.9835])
# b = np.array([0.9917,   -3.9660 ,   5.9485,   -3.9660 ,   0.9917])
# # # Time axis in units of milliseconds:

# b = np.array([0.9900,   -3.9199,    5.8602,   -3.9199,    0.9900])
# a = np.array([ 1.0000 ,  -3.9396 ,   5.8601  , -3.9001,    0.9801])

# all pass:
b = [0.9835,   -3.9305 ,   5.8941 ,  -3.9305,    0.9835]
a = [ 1.0000,   -3.9633 ,   5.8938,   -3.8978 ,   0.9672]

line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(t)                         # x-data of plot (time)

# Create block (initialize to zero)
output_block = [0 for n in range(0, BLOCKSIZE)]
Y = [ 0.0 for i in range(0, filter_order+1) ] 
X = [ 0.0 for i in range(0, filter_order+1) ] 

# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True)

input_tuple = [0 for n in range(0,BLOCKSIZE*CHANNELS)]
for i in range(0, BLOCKSIZE):

    input_string = wf.readframes(BLOCKSIZE)                     # Read audio input stream
    input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)    # Convert

    # output_block = signal.filtfilt(b,a,input_tuple)
    
    # Go through data
    for n in range(0, len(input_tuple)):
        # input_tuple[n] = input_tuple[n]*cmath.exp(I*2*math.pi*n*20/RATE)

        X[4] = input_tuple[n]
        # print X
        # original
        Yvalue = a[1] * Y[3] + a[2] * Y[2] + a[3] * Y[1] + a[4] * Y[0]
        Y[4] = b[0] * X[4] + b[1] * X[3] + b[2] * X[2] + b[3] * X[1] + b[4] * X[0] - Yvalue
        # print type(Y)
        # new
        # Yvalue = a[1] * Y[0] + a[2] * Y[1] + a[3] * Y[2] + a[4] * Y[3]
        # Y[4] = b[0] * X[0] + b[1] * X[1] + b[2] * X[2] + b[3] * X[3] + b[4] * X[4] - Yvalue
        Y[0] = np.real(Y[1])
        Y[1] = np.real(Y[2])
        Y[2] = np.real(Y[3])
        Y[3] = np.real(Y[4])
        X[0] = np.real(X[1])
        X[1] = np.real(X[2])
        X[2] = np.real(X[3])
        X[3] = np.real(X[4])
        output_block[n] =  np.real(Y[4]) 
        # print type(output_block)
        # shift array
        # shift_array(Y,1)
        # shift_array(X,1)
    # # print 'aaaa\n'
    # print output_block                             # Update y-data of plot

    output_block_fft = np.fft.fft(output_block,RATE*2)
    # output_block_fft = np.fft.fft(output_block,RATE*2)
    # print (output_block_fft),'aaa\n'
    print np.log10(output_block_fft[50:70])

    line.set_ydata(np.log10(abs(output_block_fft))*20)        
    plt.draw()
    
    # np.array(output_block).tolist()
    for n in range(0,BLOCKSIZE):
        # output_block[n] = int(output_block[n])
        output_block[n] = myfunctions.clip16(np.real(output_block[n]))
    # Convert values to binary string
    
    output_string = struct.pack('h' * BLOCKSIZE, *output_block)
    # output_string = struct.pack('h' * BLOCKSIZE, *input_tuple)
    stream.write(output_string)

plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print '* Done'
