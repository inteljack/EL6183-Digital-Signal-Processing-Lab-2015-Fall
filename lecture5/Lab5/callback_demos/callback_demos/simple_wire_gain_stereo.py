# simple_wire_gain_stereo.py
# Play microphone input to speaker using callback function
#
# Like simple_wire_gain.py, but additionally applies different gains
# to each channel of a stereo signal.

import pyaudio
import struct
import time
from myfunctions import clip16

CHANNELS = 2
RATE = 16000
gain_L = 1.0
gain_R = 0.2

# Define callback function
def my_callback_fun(input_string, block_size, time_info, status):

    N = block_size      # Number of frames
    
    # Convert string to tuple of numbers
    input_block = struct.unpack('h'*2*N, input_string)  # 2*N for stereo

    # Create output (initialize to zero)
    output_block = [0.0 for n in range(2*N)]

    for n in range(N):
        output_block[2*n]   = clip16( gain_L * input_block[2*n] )
        output_block[2*n+1] = clip16( gain_R * input_block[2*n+1] )

    # Convert output values to binary string
    output_string = struct.pack('h'*2*N, *output_block)  # 2*N for stereo

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

# Keep the stream active for 6 seconds by sleeping here
time.sleep(6.0)

stream.stop_stream()
stream.close()
p.terminate()
