from scipy.signal import butter, lfilter

import pyaudio
import struct
import math
from myfunctions import clip16, clip16_arr,clip16_flt
import numpy as np
def get_type_convert(np_type):
   convert_type = type(np.zeros(1,np_type).tolist()[0])
   return (convert_type)


def fuzz_effect():


    RECORD_SECONDS = 10
    BLOCKSIZE = 1024     # Number of frames per block
    p = pyaudio.PyAudio()
    WIDTH = 2           # bytes per sample
    RATE = 44100    # Sampling rate (samples/second)
    mix = 1 
    gain = 11 
    
    number_of_devices = p.get_device_count()
    print('There are {0:d} devices'.format(number_of_devices))
    property_list = ['defaultSampleRate', 'maxInputChannels', 'maxOutputChannels']
    for i in range(0, number_of_devices):
        print('Device {0:d} has:'.format(i))
        for s in property_list:
            print ' ', s, '=', p.get_device_info_by_index(i)[s]

    stream = p.open(format = p.get_format_from_width(WIDTH),
                    channels = 2,
                    rate = RATE,
                    input = True,
                    output = True)

    

    output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]


    q = 0.0
    X = 0.0	
    y = 0.0
    z = 0.0
    r = 0.0
    max_z = 0
    max_r = 0
    # k = 0.0


    output_all = ''            # output signal in all (string)



    num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)
    print ('* Playing...')

    # Loop through wave file 
    for i in range(0, num_blocks):


    	# Get sample from wave file
        input_string = stream.read(BLOCKSIZE)

        # Convert string to number
        input_value = struct.unpack('hh'* BLOCKSIZE, input_string)

        X = np.fft.fft(input_value)
    	max_val = abs(np.max(X))
    	# print type(max_val)
        max_val = max_val.item()
        # print type(max_val)
        # max_val = int(max_val)

        for n in range(0, BLOCKSIZE):
            x = input_value[2*n]
            q = x * gain / max_val


            if q == 0:
                z = 0
            else:
                z = -q/abs(q) * (1 - math.exp(-q*q/abs(q)))
                
            if z>max_z:
                max_z = z

        	r = mix * z * max_val/abs(max_z) + (1 - mix) * x
            # k = np.asscalar(r)
            if r>max_r:
                max_r = r

            if abs(max_r) ==0:
                out = 0
            else:
                out = r * abs(x) / abs(max_r)
            output_block[2*n] = clip16_flt(out)
            output_block[2*n+1] = clip16_flt(out)



        output_string = struct.pack('hh'* BLOCKSIZE , *output_block)

        # Write output to audio stream
        stream.write(output_string)

        output_all = output_all + output_string


    print('* Done')

    stream.stop_stream()
    stream.close()
    p.terminate()

fuzz()



