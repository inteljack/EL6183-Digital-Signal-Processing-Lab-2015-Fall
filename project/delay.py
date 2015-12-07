# feedbackdelay_circbuffer1.py
# Reads a specified wave file (mono) and plays it with a delay with feedback.
# This implementation uses a circular buffer (of minimum
# length) and one buffer index.

import pyaudio
import wave
import struct
import math
from myfunctions import clip16,clip16_arr
import sys

def delay_effect():
    BLOCKSIZE = 1024     # Number of frames per block

    RECORD_SECONDS = 20
    delay_sec = 0.5
    p = pyaudio.PyAudio()
    WIDTH = 2           # bytes per sample
    RATE = 44100    # Sampling rate (samples/second)

    d = int( math.floor( RATE * delay_sec ) ) 
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
    delay_buff = [0.0 for n in range(0, d)]




    num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)

 


    k = 0

    print ("**** Playing ****")

    for i in range(0, num_blocks):
        # Get sample from wave file
        input_string = stream.read(BLOCKSIZE)

        # Convert string to number
        input_value = struct.unpack('hh'* BLOCKSIZE, input_string)

        # t = t + 1
        # if t == 2:
        #     delay = input_value
        #     t = 0

        for n in range(0, BLOCKSIZE):

            # Update buffer
            delay_buff[k] = input_value[2*n] + Gfb * delay_buff[k]
            k = k + 1
            if k == d:
                # We have reached the end of the buffer. Circle back to front.
                k = 0
            output_block[2*n] = Gdp * input_value[2*n] + Gff * delay_buff[k];
            output_block[2*n] = clip16(output_block[2*n])
            output_block[2*n+1] = clip16(output_block[2*n])



            # # Compute output value
            # delay[n] = input_value[2*(n-d)] + Gfb * delay[(n-d)]
            # output_block[2*n] = Gdp * input_value[2*n] + Gff * delay[n]
            # output_block[2*n] = cli p16(output_block[2*n])
            # output_block[2*n+1] = clip16(output_block[2*n])
            # # if output_value <= 0.1:
            #    break
            # delay[n] = input_value[2*(n-d)]
            # output_block[2*n] = Gdp * input_value[2*n] + Gff * delay[n]

            # # output_block[2*n] = Gfb*output_block[2*(n-d)] + input_value[2*n] + (Gff-Gfb)*input_value[2*(n-d)]
            # output_block[2*n] = clip16(output_block[2*n])
            # output_block[2*n+1] = clip16(output_block[2*n])
        



        # for n in range(0,BLOCKSIZE):
        #     # output_block[2*n] = input_value[2*n]*Gdp + Gff * buffer[n];
        #     # output_block[2*n+1] = input_value[2*n]*Gdp + Gff * buffer[n];
        #     output_block[2*n] = input_value[2*n]*Gdp
        #     buffer[n] = input_value[2*n] + Gfb * buffer[n]
        


        # # output_bolck = clip16_arr(output_block)+ Gff*buffer

        # output_block = [x + y for x, y in zip(clip16_arr(output_block), Gff * clip16_arr(buffer))]






        # Clip output value to 16 bits and convert to binary string
        output_string = struct.pack('hh'* BLOCKSIZE , *output_block)

        # Write output value to audio stream
        stream.write(output_string)



    print("**** Done ****")


    stream.stop_stream()
    stream.close()
    p.terminate()

delay_effect()