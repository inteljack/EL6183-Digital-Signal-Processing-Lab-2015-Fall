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
from myfunctions import clip16

wavfile = 'author.wav'
# wavfile = 'decay_cosine_mono.wav'
print 'Play the wave file: {0:s}.'.format(wavfile)

# Open wave file
wf = wave.open( wavfile, 'rb')

# Number of frames per block
BLOCKSIZE = 256

# Read wave file properties
CHANNELS = wf.getnchannels()        # Number of channels
RATE = wf.getframerate()            # Sampling rate (frames/second)
LEN  = wf.getnframes()              # Signal length
WIDTH = wf.getsampwidth()           # Number of bytes per sample

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)

# Vibrato parameters
f0 = 10
W = 0.7     # W = 0 # for no effct
gain = 0.9

# Create a buffer (delay line) for past values
buffer = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero

# Buffer (delay line) indices
kr = 0  # read index
kw = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
kw = BLOCKSIZE/2

# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print 'The buffer is {0:d} samples long.'.format(BLOCKSIZE)

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 2,
                rate        = RATE,
                input       = False,
                output      = True )

# Create block (initialize to zero)
output_block = [0 for n in range(0, 2*BLOCKSIZE)]

# Number of blocks in wave file
num_blocks = int(math.floor(LEN/BLOCKSIZE))

# Initialize angle
theta = 0.0

# Block-to-block angle increment
theta_del = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi


output_all = ''            # output signal in all (string)

print ('* Playing...')

# Loop through wave file 
for n in range(0, num_blocks):

    # Get sample from wave file
    input_string = wf.readframes(BLOCKSIZE)

    # Convert binary string to tuple of numbers    
    input_value = struct.unpack('h' * BLOCKSIZE, input_string)

    # Go through block
    for n in range(0, BLOCKSIZE):

        # Get previous and next buffer values (since kr is fractional)
        kr_prev = int(math.floor(kr))               
        kr_next = (kr_prev + 1) % BLOCKSIZE
        frac = kr - kr_prev    # 0 <= frac < 1
        # if kr_next >= BLOCKSIZE:
        #     kr_next = kr_next - BLOCKSIZE

        # Compute output value using interpolation
        prev = (1-frac) * buffer[kr_prev]
        nextt = frac * buffer[kr_next]
        # output_block[n] = prev + nextt
        output_block[2*n] = (prev + nextt) * gain + input_value[n]
        output_block[2*n+1] = (prev + nextt) * gain + input_value[n]

        output_block[2*n] = clip16(output_block[2*n])
        output_block[2*n+1] = clip16(output_block[2*n+1])

        # Update buffer (pure delay)
        buffer[kw] = input_value[n]

        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE + theta)
            # Note: kr is fractional (not integer!)

        # Ensure that 0 <= kr < BLOCKSIZE
        if kr >= BLOCKSIZE:
            # End of buffer. Circle back to front.
            kr = 0

        # Increment write index    
        kw = kw + 1
        if kw == BLOCKSIZE:
            # End of buffer. Circle back to front.
            kw = 0
    # Set angle for next block
    theta = theta + theta_del

    # Convert values to binary string
    output_string = struct.pack('hh' * BLOCKSIZE, *output_block)

    # Write output to audio stream
    stream.write(output_string)

    output_all = output_all + output_string     # append new to total

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()

output_wavefile = wavfile[:-4] + '_vibrato.wav'
print 'Writing to wave file', output_wavefile
wf = wave.open(output_wavefile, 'w')      # wave file
wf.setnchannels(1)      # one channel (mono)
wf.setsampwidth(2)      # two bytes per sample
wf.setframerate(RATE)   # samples per second
wf.writeframes(output_all)
wf.close()
print('* Done')

