from scipy.signal import butter, lfilter

import pyaudio
import struct
import math
import numpy as np
from myfunctions import clip16, clip16_arr


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def wah_effect(f_lfo,fc_min,w):


    RECORD_SECONDS = 10
    BLOCKSIZE = 1024     # Number of frames per block
    
    gain = 1
    # w = 1

    # f_lfo = 0.2
    fc_min = 250
    fc_max = 1200 # initial
    # fc = fc_min

    p = pyaudio.PyAudio()
    WIDTH = 2           # bytes per sample
    RATE = 44100    # Sampling rate (samples/second)

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

    # Create a buffer (delay line) for past values
    # Create block (initialize to zero)
    output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]
    output_block_filt = [0.0 for n in range(0, 2*BLOCKSIZE)]
    bandpass = [0.0 for n in range(0, 2*BLOCKSIZE)]
    mix = [0.0 for n in range(0, 2*BLOCKSIZE)]


    # Create a buffer (delay line) for past values
    # buffer_MAX =  1024                          # Buffer length
    buffer = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero
    buffer2 = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero

    # Buffer (delay line) indices
    kr = 0  # read index
    kw = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
    kw = BLOCKSIZE/2

    # Buffer (delay line) indices
    # kr2 = 0  # read index
    # kw2 = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
    # kw2 = BLOCKSIZE/2



    output_all = ''            # output signal in all (string)
    fc_bandpass = 0.0

    # Initialize angle
    theta = 0.0
    # theta2 = 0.0

    # Block-to-block angle increment
    theta_del = (float(BLOCKSIZE*f_lfo)/RATE - math.floor(BLOCKSIZE*f_lfo/RATE)) * 2.0 * math.pi
    # theta_del2 = (float(BLOCKSIZE*f1)/RATE - math.floor(BLOCKSIZE*f1/RATE)) * 2.0 * math.pi
    num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)

    print ('* Playing...')

    # Loop through wave file 
    for i in range(0, num_blocks):
        # Get sample from wave file
        input_string = stream.read(BLOCKSIZE)

        # Convert string to number
        input_value = struct.unpack('hh'* BLOCKSIZE, input_string)


        # X = np.fft.fft(input_value)
        # dB = 20 * np.log10(abs(X))


        # if np.max(dB) > 80:
        #     fc = 800
        # else:
        #     fc = 400
        # 100 ,900

        # 400 , 2000

        # 400 , 1200
        # fc = (f_max - f_min) / 2
        # f_max = 2 * fc + f_min

        bandpass = butter_bandpass_filter(input_value,fc_min,fc_max,RATE,order = 1)
        # # Get previous and next buffer values (since kr is fractional)
        # fc_bandpass = fc_bandpass + delta

        # if fc_bandpass >= fc_max:
        #     delta = -delta
        # if fc_bandpass <= fc_min:
        #     delta = -delta


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
            k2 = buffer2[kr_prev] * (1-frac)
            r2 = buffer2[kr_next] * frac
        	# butter_bandpass_filter(data, lowcut, highcut, fs, order=5):



            # output_block[2*n] = butter_bandpass_filter(mix[2*n],500.0,3000.0,2000,order = 5) + mix[2*n]
            output_block[2*n] = k + r + k2 +r2
            output_block[2*n] = clip16(output_block[2*n])
            output_block[2*n+1] = output_block[2*n]

            # buffer
            # print '--------------'
            buffer[kw] = input_value[2*n]
            buffer2[kw] = bandpass[2*n]
            # Increment read index
            kr = kr + 1 + w * math.sin( 2 * math.pi * f_lfo * n  / RATE + theta)     
            # Note: kr is fractional (not integer!)
            # f = fl_min + delta_lfo


            # Ensure that 0 <= kr < buffer_MAX
            if kr >= BLOCKSIZE:
            # End of buffer. Circle back to front.
                kr = 0
            # Increment write index    
            kw = kw + 1
            if kw == BLOCKSIZE:
             # End of buffer. Circle back to front.
                kw = 0

            fc_bandpass = fc_min + 0.5 * w * (1 + math.sin(2 * math.pi * f_lfo * n /RATE ))
            f_max = 2 * fc_bandpass + fc_min

        theta = theta + theta_del




        # print output_block
        # output_block[2*n] = butter_bandpass_filter(mix[2*n],500.0,3000.0,2000,order = 5) + mix[2*n]

        # if fc >=fc_max:
        # 	fc =  fc_min
        # output_block_filt = butter_bandpass_filter(output_block,fc,3000.0,2000,order = 5)
        # # output_block = clip16_arr(output_block) + clip16_arr(output_block_filt)
        # fc = fc_min + 200
        # output_block = [x + y for x, y in zip(clip16_arr(output_block_filt), output_block)]
        





        # output_block = clip16_arr(output_block)


        output_string = struct.pack('hh'* BLOCKSIZE , *output_block)


        # output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]

        # Write output to audio stream
        stream.write(output_string)

        output_all = output_all + output_string


    print('* Done')

    stream.stop_stream()
    stream.close()
    p.terminate()


wah_effect(2,1000,0.05)


# flanger(1,1)
