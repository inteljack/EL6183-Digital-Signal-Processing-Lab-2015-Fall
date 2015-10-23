# using callback

# Assignment: modify so block size (buffer size) is longer than one sample.

import pyaudio, struct
import wave
import time
import math
from myfunctions import clip16, play_wav
import os
import sys
file_name =  os.path.basename(sys.argv[0])

filename = file_name[:-3] + '_record.wav'

RATE = 16000    # sampling rate
CHANNELS = 1    # stereo
WIDTH = 2       # bytes per sample
GAIN = 0.5
BLOCKSIZE = 1024

# Create a buffer (delay line) for past values
buffer_MAX =  1024                          # Buffer length
buffer = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

# Create block (initialize to zero)
output_block = [0 for n in range(0, BLOCKSIZE)]
output_string = ""
out_value = [0.0 for n in range(BLOCKSIZE)]

# Vibrato parameters
f0 = 2
W = 0.2

# Buffer (delay line) indices
kr = 0  # read index
kw = int(0.5 * buffer_MAX)      # write index (initialize to middle of buffer)
n = 0


# Define call back for vibrato effect
def my_callback(input_string, block_size, time_info, status):
    global kr, kw, n
    # Create output (initialize to zero)
    
    in_sample = struct.unpack('h' * block_size, input_string)
    
    for i in range(0,block_size):
        out_sample = buffer[int(kr)]
        buffer[kw] = in_sample[i]

        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE)
            # Note: kr is not integer!

        # Ensure that 0 <= kr < buffer_MAX
        if kr >= buffer_MAX:
            # End of buffer. Circle back to front.
            kr = 0

        # Increment write index    
        kw = kw + 1
        if kw == buffer_MAX:
            # End of buffer. Circle back to front.
            kw = 0
        out_value[i] = clip16( GAIN * out_sample)
        n+=1
        output_data.append(out_value[i])
    # Convert output values to binary string
    output_string = struct.pack('h'*block_size, *out_value)
    return (output_string, pyaudio.paContinue)

p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                stream_callback = my_callback)

output_data = []

print '* Recording 5 seconds ...'

time.sleep(5.0)

stream.stop_stream()
print 'Done.'

stream.close()
p.terminate()

# Convert output signal to binary string
output_string = struct.pack('h'*len(output_data), *output_data)

# Write data to wave file
wf = wave.open(filename, 'w')
wf.setnchannels(CHANNELS)
wf.setsampwidth(WIDTH)
wf.setframerate(RATE)
wf.writeframes(output_string)
wf.close()

# Play wave file
play_wav(filename)
