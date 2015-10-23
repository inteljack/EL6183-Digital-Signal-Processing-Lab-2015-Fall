# recplayAM_mono.py
# Record audio and play it with amplitude modulation. 
# This implementation:
#   uses blocking, 
#   corrects for block-to-block angle mismatch,
#   assumes mono channel
"""
Read a signal from a wave file, do amplitude modulation, play to output
Original: pyrecplay_modulation.py by Gerald Schuller, Octtober 2013
Modified to read a wave file - Ivan Selesnick, September 2015
"""

import pyaudio
import struct
import math
import wave
import sys    
import os
file_name =  os.path.basename(sys.argv[0])

f0 = 0      # Normal audio
f1 = 200
#f0 = 400    # 'Duck' audio

BLOCKSIZE = 1024  # Number of frames per block

WIDTH = 2       # Number of bytes per sample
CHANNELS = 2    # stereo
RATE = 32000    # Sampling rate (samples/second)
RECORD_SECONDS = 5

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

#Initialize block
output_block = [0 for i in range(0, 2*BLOCKSIZE)]

# Initialize angle
theta0 = 0.0
theta1 = 0.0

# Block-to-block angle increment
theta_del0 = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi
theta_del1 = (float(BLOCKSIZE*f1)/RATE - math.floor(BLOCKSIZE*f1/RATE)) * 2.0 * math.pi

# Number of blocks to run for
num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)

# output signal in all (string)
output_all = ''            

print('* Recording for {0:.3f} seconds'.format(RECORD_SECONDS))

# Start loop
for i in range(0, num_blocks):

    # Get frames from audio input stream
    input_string = stream.read(BLOCKSIZE)       # BLOCKSIZE = number of frames read

    # Convert binary string to tuple of numbers
    input_tuple = struct.unpack('hh' * BLOCKSIZE, input_string)
   
    # Go through block
    for n in range(0, BLOCKSIZE):
        # No processing:
        # output_block[n] = input_tuple[n]  
        # OR
        # Amplitude modulation:
        output_block[2*n] = input_tuple[2*n] * math.cos(2*math.pi*n*f0/RATE + theta0)
        output_block[2*n+1] = input_tuple[2*n+1] * math.cos(2*math.pi*n*f1/RATE + theta1)

    # Set angle for next block
    theta0 = theta0 + theta_del0
    theta1 = theta1 + theta_del1

    # Convert values to binary string
    output_string = struct.pack('hh' * BLOCKSIZE, *output_block)

    # Write binary string to audio output stream
    stream.write(output_string)
    
    # append new to total
    output_all = output_all + output_string

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