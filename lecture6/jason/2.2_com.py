# playAM_blocking_fix.py
# Play a mono wave file with amplitude modulation. 
# This implementation reads and plays a block at a time (blocking)
# and corrects for block-to-block angle mismatch.
# Assignment: modify file so it works for both mono and stereo wave files
#  (where does this file have an error when wave file is stereo and why? )
"""
Read a signal from a wave file, do amplitude modulation, play to output
Original: pyrecplay_modulation.py by Gerald Schuller, Octtober 2013
Modified to read a wave file - Ivan Selesnick, September 2015
"""

# f0 = 0      # Normal audio
f0 = 400    # 'Duck' audio

BLOCKSIZE = 64      # Number of frames per block
import numpy as np
import pyaudio
import struct
import wave
import math
import cmath
from myfunctions import clip16

# Open wave file (mono)
wave_file_name = 'onceupon.wav'
# wave_file_name = 'sin01_mono.wav'
# wave_file_name = 'sin01_stereo.wav'
wf = wave.open( wave_file_name, 'rb')
RATE = wf.getframerate()
WIDTH = wf.getsampwidth()
LEN = wf.getnframes() 
CHANNELS = wf.getnchannels() 

print 'The sampling rate is {0:d} samples per second'.format(RATE)
print 'Each sample is {0:d} bytes'.format(WIDTH)
print 'The signal is {0:d} samples long'.format(LEN)
print 'The signal has {0:d} channel(s)'.format(CHANNELS)

# Open audio stream
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = 1,
                rate = RATE,
                input = False,
                output = True)


# print 'rate', RATE

# Create block (initialize to zero)
output_block = [0 for n in range(0, BLOCKSIZE)]

# Number of blocks in wave file
num_blocks = int(math.floor(LEN/BLOCKSIZE))
# I = np.sqrt(-1)

# Initialize angle
theta = 0.0

# Block-to-block angle increment
theta_del = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi

print('* Playing...')

# Go through wave file 
for i in range(0, num_blocks):

    # Get block of samples from wave file
    input_string = wf.readframes(BLOCKSIZE)     # BLOCKSIZE = number of frames read

    # Convert binary string to tuple of numbers    
    input_tuple0 = struct.unpack('h' * BLOCKSIZE, input_string)
            # (h: two bytes per sample (WIDTH = 2))
    input_tuple_r = np.fft.rfft(input_tuple0)
    input_tuple = np.fft.irfft(input_tuple_r)

    # input_tuple = input_tuple0 - input_tuple_ir

    # print 'rfft:' ,input_tuple
    # Go through block
    for n in range(0, BLOCKSIZE):
        # Amplitude modulation  (f0 Hz cosine)
        # print 'theta',theta
        # print 'exp:',2*cmath.sqrt(-1)*math.pi*n*f0/RATE
        m = cmath.exp(2*cmath.sqrt(-1)*math.pi*n*f0/RATE)
        output_block[n] = input_tuple[n] * m
        r = output_block[n]
        real_val = r.real * math.cos(theta)
        # print real_val
        # out
        # print output_block
        # print type(output_block)
        # output_block[n] = input_tuple[n] * 1.0  # for no processing
        # output_block[n] = output_block[n]

        output_block[n] = clip16(real_val)
    # print output_block

    # Set angle for next block
    theta = theta + theta_del
    # print output_block
    # Convert values to binary string
    output_string = struct.pack('h' * BLOCKSIZE, *output_block)

    # Write binary string to audio output stream
    stream.write(output_string)

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()
