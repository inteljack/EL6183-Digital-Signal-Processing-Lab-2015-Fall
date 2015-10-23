# play_vibrato_interpolation.py
# Reads a specified wave file (mono) and plays it with a vibrato effect
# (sinusoidal time-varying delay).
# This implementation:
#   uses a circular buffer with two buffer indices,
#   uses linear interpolation,
#   saves output as a wave file

import pyaudio
import wave
import struct
import math
import sys    
import os
from myfunctions import clip16
file_name =  os.path.basename(sys.argv[0])

# Number of frames per block
BLOCKSIZE = 128

WIDTH = 2       # Number of bytes per sample
CHANNELS = 2    # mono
RATE = 32000    # Sampling rate (samples/second)
RECORD_SECONDS = 8

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d seconds.'            % RECORD_SECONDS)
print('The file has %d bytes per sample.'   % WIDTH)

# Vibrato parameters
f0 = 2
f1 = 0
W0 = 0.4
W1 = 0
# W = 0 # for no effct

p = pyaudio.PyAudio()

number_of_devices = p.get_device_count()
print('There are {0:d} devices'.format(number_of_devices))

property_list = ['defaultSampleRate', 'maxInputChannels', 'maxOutputChannels']
for i in range(0, number_of_devices):
    print('Device {0:d} has:'.format(i))
    for s in property_list:
        print ' ', s, '=', p.get_device_info_by_index(i)[s]

stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True)

# Create two buffers (delay line) for past values
buffer0 = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero
buffer1 = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero

# Buffer 0 (delay line) indices
kr0 = 0  # read index
kw0 = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
kw0 = BLOCKSIZE/2

# Buffer 1 (delay line) indices
kr1 = 0  # read index
kw1 = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
kw1 = BLOCKSIZE/2

# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print 'The buffer is {0:d} samples long.'.format(BLOCKSIZE)

# Create block (initialize to zero)
output_block = [0.0 for n in range(0, CHANNELS*BLOCKSIZE)]

# Number of blocks to run for
num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)

# Initialize angle
theta0 = 0.0
theta1 = 0.0

# Block-to-block angle increment
theta_del0 = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi
theta_del1 = (float(BLOCKSIZE*f1)/RATE - math.floor(BLOCKSIZE*f1/RATE)) * 2.0 * math.pi

output_all = ''            # output signal in all (string)

print ('* Playing...')

# Loop through wave file 
for n in range(0, num_blocks):

    # Get sample from wave file
    input_string = stream.read(BLOCKSIZE)

    # Convert binary string to tuple of numbers    
    input_value = struct.unpack('hh' * BLOCKSIZE, input_string)

    # Go through block
    for n in range(0, BLOCKSIZE):

        # Get previous and next buffer values (since kr is fractional)
        kr_prev0 = int(math.floor(kr0))               
        kr_next0 = (kr_prev0 + 1) % BLOCKSIZE
        frac0 = kr0 - kr_prev0    # 0 <= frac < 1
        # if kr_next0 >= BLOCKSIZE:
        #     kr_next0 = kr_next0 - BLOCKSIZE

        # Compute output value using interpolation
        prev0 = (1-frac0) * buffer0[kr_prev0]
        next0 = frac0 * buffer0[kr_next0]

        # Get previous and next buffer values (since kr is fractional)
        kr_prev1 = int(math.floor(kr1))               
        kr_next1= (kr_prev1 + 1) % BLOCKSIZE
        frac1 = kr1 - kr_prev1    # 0 <= frac < 1
        # if kr_next1 >= BLOCKSIZE:
        #     kr_next1 = kr_next1 - BLOCKSIZE

        # Compute output value using interpolation
        prev1 = (1-frac1) * buffer1[kr_prev1]
        next1 = frac1 * buffer1[kr_next1]

        output_block[2*n] = prev0 + next0
        output_block[2*n+1] = prev1 + next1

        # Update buffer (pure delay)
        buffer0[kw0] = input_value[2*n]
        buffer1[kw1] = input_value[2*n+1]

        # Increment read index
        kr0 = kr0 + 1 + W0 * math.sin( 2 * math.pi * f0 * n / RATE + theta0)
        kr1 = kr1 + 1 + W1 * math.sin( 2 * math.pi * f1 * n / RATE + theta1)
            # Note: kr is fractional (not integer!)

        # Ensure that 0 <= kr < BLOCKSIZE
        if kr0 >= BLOCKSIZE:
            # End of buffer. Circle back to front.
            kr0 = 0

        # Increment write index    
        kw0 = kw0 + 1
        if kw0 == BLOCKSIZE:
            # End of buffer. Circle back to front.
            kw0 = 0
        
        # Ensure that 0 <= kr < BLOCKSIZE
        if kr1 >= BLOCKSIZE:
            # End of buffer. Circle back to front.
            kr1 = 0

        # Increment write index    
        kw1 = kw1 + 1
        if kw1 == BLOCKSIZE:
            # End of buffer. Circle back to front.
            kw1 = 0

    # Set angle for next block
    theta0 = theta0 + theta_del0
    theta1 = theta1 + theta_del1

    # Convert values to binary string
    output_string = struct.pack('hh' * BLOCKSIZE, *output_block)

    # Write output to audio stream
    stream.write(output_string)

    output_all = output_all + output_string     # append new to total

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()

output_wavefile = file_name[:-3] + '_record.wav'
print 'Writing to wave file', output_wavefile
wf = wave.open(output_wavefile, 'w')      # wave file
wf.setnchannels(CHANNELS)      # one channel (mono)
wf.setsampwidth(2)      # two bytes per sample
wf.setframerate(RATE)   # samples per second
wf.writeframes(output_all)
wf.close()
print('* Done')

