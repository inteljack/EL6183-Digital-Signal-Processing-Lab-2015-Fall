# simple_wire_gain.py
# Play microphone input to speaker using callback function
#
# Like simple_wire.py, but additionally applies a gain 

import pyaudio
import struct
import time
from myfunctions import clip16

CHANNELS = 1
RATE = 16000        # frames / second
gain = 4.0

counter = 1

# Define callback function
def my_callback_fun(input_string, block_size, time_info, status):
    global counter
    N = block_size      # Number of frames
    if counter > 0:
        print 'block size is',block_size
        counter = counter -1
    # Convert string to tuple of numbers
    input_block = struct.unpack('h'*N, input_string)

    # Create output (initialize to zero)
    output_block = [0.0 for n in range(N)]

    for n in range(N):
        output_block[n] = clip16(gain * input_block[n])

    # Convert output values to binary string
    output_string = struct.pack('h'*N, *output_block)

    return (output_string, pyaudio.paContinue)    # Return data and status


# Create audio object
p = pyaudio.PyAudio()

# Open stream using callback
stream = p.open(format = pyaudio.paInt16,       # 16 bits/sample
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                stream_callback = my_callback_fun)

stream.start_stream()

print 'The wire will be on for 6 seconds'
# Keep the stream active for 6 seconds by sleeping here
time.sleep(6)

stream.stop_stream()
stream.close()
p.terminate()

