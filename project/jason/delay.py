# feedbackdelay_circbuffer1.py
# Reads a specified wave file (mono) and plays it with a delay with feedback.
# This implementation uses a circular buffer (of minimum
# length) and one buffer index.

import pyaudio
import wave
import struct
import math
from myfunctions import clip16
import sys

def delay_effect():
    BLOCKSIZE = 1024     # Number of frames per block

    RECORD_SECONDS = 10
    d = 10
    p = pyaudio.PyAudio()
    WIDTH = 2           # bytes per sample
    RATE = 44100    # Sampling rate (samples/second)

    # Set parameters of delay system
    Gfb = .55       # feed-back gain
    Gdp = 1.0       # direct-path gain
    Gff = .500     # feed-forward gain
    # Gff = 0.0         # feed-forward gain (set to zero for no effect)




    # Open an output audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format      = p.get_format_from_width(WIDTH),
                    channels    = 2,
                    rate        = RATE,
                    input       = True,
                    output      = True )

    output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]
    delay = [0.0 for n in range(0, BLOCKSIZE)]




    num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)





    print ("**** Playing ****")

    for i in range(0, num_blocks):
        # Get sample from wave file
        input_string = stream.read(BLOCKSIZE)

        # Convert string to number
        input_value = struct.unpack('hh'* BLOCKSIZE, input_string)


        for n in range(0, BLOCKSIZE):

            # # Compute output value
            # delay[n] = input_value[2*(n-d)] + Gfb * delay[(n-d)]
            # output_block[2*n] = Gdp * input_value[2*n] + Gff * delay[n]
            # output_block[2*n] = clip16(output_block[2*n])
            # output_block[2*n+1] = clip16(output_block[2*n])
            # # if output_value <= 0.1:
            #    break

            output_block[2*n] = Gfb*output_block[2*(n-d)] + input_value[2*n] + (Gff-Gfb)*input_value[2*(n-d)]
            output_block[2*n] = clip16(output_block[2*n])
            output_block[2*n+1] = clip16(output_block[2*n])


            # Increment buffer index


        # Clip output value to 16 bits and convert to binary string
        output_string = struct.pack('hh'* BLOCKSIZE , *output_block)

        # Write output value to audio stream
        stream.write(output_string)



    print("**** Done ****")


    stream.stop_stream()
    stream.close()
    p.terminate()

delay_effect()