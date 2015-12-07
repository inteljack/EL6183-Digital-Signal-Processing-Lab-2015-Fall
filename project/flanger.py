# Reads a specified wave file (mono) and plays it with a vibrato effect
# (sinusoidal time-varying delay).
# This implementation:
#   uses a circular buffer with two buffer indices,
#   uses linear interpolation,
#   saves output as a wave file
import pyaudio
import struct
import math
from myfunctions import clip16

def flanger_effect(f,w):

    BLOCKSIZE = 4096      # Number of frames per block

    # RECORD_SECONDS = 100

    # f0 = f
    # W1 = w  
    # f1 = f0
    # W2 = W1
    
    gain = 0.6

    p = pyaudio.PyAudio()
    WIDTH = 2           # bytes per sample
    RATE = 44100    # Sampling rate (samples/second)

    # number_of_devices = p.get_device_count()
    # print('There are {0:d} devices'.format(number_of_devices))
    # property_list = ['defaultSampleRate', 'maxInputChannels', 'maxOutputChannels']
    # for i in range(0, number_of_devices):
    #     print('Device {0:d} has:'.format(i))
    #     for s in property_list:
    #         print ' ', s, '=', p.get_device_info_by_index(i)[s]

    stream = p.open(format = p.get_format_from_width(WIDTH),
                    channels = 2,
                    rate = RATE,
                    input = True,
                    output = True)

    # Create a buffer (delay line) for past values
    # Create block (initialize to zero)
    output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]


    # Create a buffer (delay line) for past values
    # buffer_MAX =  1024                          # Buffer length
    buffer = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero
    # buffer2 = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero

    # Buffer (delay line) indices
    kr = 0  # read index
    kw = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
    kw = BLOCKSIZE/2

    # Buffer (delay line) indices
    # kr2 = 0  # read index
    # kw2 = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
    # kw2 = BLOCKSIZE/2


    output_all = ''            # output signal in all (string)


    # Initialize angle
    theta = 0.0
    # theta2 = 0.0

    # Block-to-block angle increment
    theta_del = (float(BLOCKSIZE*f)/RATE - math.floor(BLOCKSIZE*f/RATE)) * 2.0 * math.pi
    # theta_del2 = (float(BLOCKSIZE*f1)/RATE - math.floor(BLOCKSIZE*f1/RATE)) * 2.0 * math.pi


    print ('* Playing...')

    # Loop through wave file 
    while(1):
        # Get sample from wave file
        input_string = stream.read(BLOCKSIZE)

        # Convert string to number
        input_value = struct.unpack('hh'* BLOCKSIZE, input_string)

        # Get previous and next buffer values (since kr is fractional)


        # Go through block
        for n in range(0, BLOCKSIZE):
            # Amplitude modulation  (f0 Hz cosine)
            # Get previous and next buffer values (since kr is fractional)
            kr_prev = int(math.floor(kr))               
            kr_next = kr_prev + 1
            frac = kr - kr_prev    # 0 <= frac < 1
            #print frac
            if kr_next >= BLOCKSIZE:
                kr_next = kr_next - BLOCKSIZE

            # Compute output value using interpolation
            k = buffer[kr_prev] * (1-frac)
            r = buffer[kr_next] * frac

            output_block[2*n] = k + r + input_value[2*n] * gain

            output_block[2*n] = clip16(output_block[2*n])
            output_block[2*n+1] = output_block[2*n]

            # buffer
            # print '--------------'
            buffer[kw] = input_value[2*n]

            # Increment read index
            kr = kr + 1 + w * math.sin( 2 * math.pi * f * n  / RATE + theta)     
            # Note: kr is fractional (not integer!)

            # Ensure that 0 <= kr < buffer_MAX
            if kr >= BLOCKSIZE:
            # End of buffer. Circle back to front.
                kr = 0
            # Increment write index    
            kw = kw + 1
            if kw == BLOCKSIZE:
             # End of buffer. Circle back to front.
                kw = 0

        theta1 = theta + theta_del
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
