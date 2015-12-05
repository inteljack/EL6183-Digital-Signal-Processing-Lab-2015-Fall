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

def flanger_effect(f,w):

    BLOCKSIZE = 64      # Number of frames per block
    WIDTH = 2       # Number of bytes per sample
    CHANNELS = 2    # mono
    RATE = 32000    # Sampling rate (samples/second)

    RECORD_SECONDS = 5

    f0 = f
    W1 = w   
    f1 = f0
    W2 = W1
    
    gain = 1

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


    # Create a buffer (delay line) for past values
    # Create block (initialize to zero)
    output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]

    # Number of blocks in wave file
    num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)

    # Create a buffer (delay line) for past values
    # buffer_MAX =  1024                          # Buffer length
    buffer1 = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero
    buffer2 = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero

    # Buffer (delay line) indices
    kr1 = 0  # read index
    kw1 = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
    kw1 = BLOCKSIZE/2

    # Buffer (delay line) indices
    kr2 = 0  # read index
    kw2 = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
    kw2 = BLOCKSIZE/2


    output_all = ''            # output signal in all (string)


    # Initialize angle
    theta1 = 0.0
    theta2 = 0.0

    # Block-to-block angle increment
    theta_del1 = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi
    theta_del2 = (float(BLOCKSIZE*f1)/RATE - math.floor(BLOCKSIZE*f1/RATE)) * 2.0 * math.pi


    print ('* Playing...')

    # Loop through wave file 
    for n in range(0, num_blocks):

        # Get sample from wave file
        input_string = stream.read(BLOCKSIZE)

        # Convert string to number
        input_value = struct.unpack('hh'* BLOCKSIZE, input_string)

        # Get previous and next buffer values (since kr is fractional)


        # Go through block
        for n in range(0, BLOCKSIZE):
            # Amplitude modulation  (f0 Hz cosine)
            # Get previous and next buffer values (since kr is fractional)
            kr_prev1 = int(math.floor(kr1))               
            kr_next1 = kr_prev1 + 1
            frac1 = kr1 - kr_prev1    # 0 <= frac < 1
            #print frac
            if kr_next1 >= BLOCKSIZE:
                kr_next1 = kr_next1 - BLOCKSIZE

            # Compute output value using interpolation
            k1 = buffer1[kr_prev1] * (1-frac1)
            r1 = buffer1[kr_next1] * frac1

    #####################
            kr_prev2 = int(math.floor(kr2))               
            kr_next2 = kr_prev2 + 1
            frac2 = kr2 - kr_prev2    # 0 <= frac < 2
            #print frac
            if kr_next2 >= BLOCKSIZE:
                kr_next2 = kr_next2 - BLOCKSIZE

            # Compute output value using interpolation
            k2 = buffer2[kr_prev2] * (1-frac2)
            r2 = buffer2[kr_next2] * frac2
            
            
            output_block[2*n] = k1 + r1 + input_value[2*n] * gain
            output_block[2*n+1] = k2 + r2 + input_value[2*n+1] * gain

            output_block[2*n] = clip16(output_block[2*n])
            output_block[2*n+1] = clip16(output_block[2*n+1])

            # buffer
            # print '--------------'
            buffer1[kw1] = input_value[2*n]
            buffer2[kw2] = input_value[2*n+1]

            # Increment read index
            kr1 = kr1 + 1 + W1 * math.sin( 2 * math.pi * f0 * n  / RATE + theta1)
            kr2 = kr2 + 1 + W2 * math.sin( 2 * math.pi * f1 * n  / RATE + theta2)
           
            # Note: kr is fractional (not integer!)

            # Ensure that 0 <= kr < buffer_MAX
            if kr1 >= BLOCKSIZE:
            # End of buffer. Circle back to front.
                kr1 = 0
            # Increment write index    
            kw1 = kw1 + 1
            if kw1 == BLOCKSIZE:
             # End of buffer. Circle back to front.
                kw1 = 0

            # Ensure that 0 <= kr < buffer_MAX
            if kr2 >= BLOCKSIZE:
            # End of buffer. Circle back to front.
                kr2 = 0
            # Increment write index    
            kw2 = kw2 + 1
            if kw2 == BLOCKSIZE:
             # End of buffer. Circle back to front.
                kw2 = 0

        theta1 = theta1 + theta_del1
        theta2 = theta2 + theta_del2
        # print output_block

        output_string = struct.pack('hh'* BLOCKSIZE , *output_block)

        # Write output to audio stream
        stream.write(output_string)

        output_all = output_all + output_string      


    print('* Done')

    stream.stop_stream()
    stream.close()
    p.terminate()

# flanger(1,1)
