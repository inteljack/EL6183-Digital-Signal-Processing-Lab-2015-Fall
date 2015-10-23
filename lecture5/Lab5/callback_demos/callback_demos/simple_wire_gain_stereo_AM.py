# simple_wire_gain_stereo_AM.py
# Play microphone input to speaker using callback function
#
# Like simple_wire_gain_stereo.py, but additionally applies
# time-varying sinusoidal gain with different phases in each channel.
# The audio signal shifts between channels.

import pyaudio
import struct
import time
import math


CHANNELS = 2        # Number of channesl
RATE = 16000        # Frame rate (frames/second)
f0 = 0.5            # Frequency (Hz) of cos/sin amplitude modulation
ph = 0                                  # Initial phase
ph_del = 2.0 * math.pi * f0 / RATE      # Phase increment

# Define callback function
def my_callback_fun(input_string, block_size, time_info, status):
    global ph, ph_del

    N = block_size      # Number of frames
    
    # Convert string to tuple of numbers
    input_block = struct.unpack('h'*2*N, input_string)  # 2*N for stereo

    # Create output (initialize to zero)
    output_block = [0.0 for n in range(2*N)]

    for n in range(N):
        output_block[2*n]   = math.sin(ph) * input_block[2*n]
        output_block[2*n+1] = math.cos(ph) * input_block[2*n+1]
        ph = ph + ph_del

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
time.sleep(10.0)

stream.stop_stream()
stream.close()
p.terminate()
