# record_and_play_vibrato.py
# using callback

# Assignment: modify so block size (buffer size) is longer than one sample.

import pyaudio, struct
import wave
import time
import math
from myfunctions import clip16, play_wav

filename = 'test_vibrato.wav'

RATE = 16000    # sampling rate
CHANNELS = 1    # stereo
WIDTH = 2       # bytes per sample
GAIN = 0.5

BLOCKSIZE = 1024
# Create a buffer (delay line) for past values
buffer_MAX =  1024                          # Buffer length
buffer = [0.0 for i in range(buffer_MAX)]   # Initialize to zero
output_data = []
# Vibrato parameters
f0 = 2
W = 0.2

# Buffer (delay line) indices
n = 0
kr = 0  # read index
kw = int(0.5 * buffer_MAX)      # write index (initialize to middle of buffer)

# Define call back for vibrato effect
def my_callback(input_string, block_size, time_info, status):
    global n, kr, kw
    # print kr
    print "******"
    output_string = ""
    in_sample = struct.unpack('h' * BLOCKSIZE, input_string)
    # print len(in_sample)
    sample = [0.0 for i in range(buffer_MAX)]
    buffer = [0.0 for i in range(buffer_MAX)]
    output_data = [0.0 for i in range(buffer_MAX)]
    for i in range(0,BLOCKSIZE):
        out_sample = buffer[int(kr)]
        buffer[kw] = in_sample[i]
    
        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
        # print kr
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
        # time.sleep(0.01)
        # out_sample[i] = int(out_sample[i])
        # print out_sample
        sample[i] = clip16( GAIN * (out_sample) )
        output_data[i] = sample[i]
        n+=1
    output_string+=( struct.pack('h'*len(output_data), *output_data))
    return (output_string, pyaudio.paContinue)

p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                # frames_per_buffer = 1,
                stream_callback = my_callback)



print '* Recording 5 seconds ...'

time.sleep(5.0)

stream.stop_stream()
print 'Done.'

stream.close()
p.terminate()

# Convert output signal to binary string
# output_string = struct.pack('h'*len(output_data), *output_data)

# Write data to wave file
# wf = wave.open(filename, 'w')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(WIDTH)
# wf.setframerate(RATE)
# wf.writeframes(output_string)
# wf.close()

# # Play wave file
# play_wav(filename)
