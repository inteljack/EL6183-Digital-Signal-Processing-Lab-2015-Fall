from scipy.signal import butter, lfilter

import pyaudio
import struct
import math
from myfunctions import clip16, clip16_arr


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def wah_effect():

    RECORD_SECONDS = 10
    BLOCKSIZE = 256     # Number of frames per block
    p = pyaudio.PyAudio()
    WIDTH = 2           # bytes per sample
    RATE = 44100    # Sampling rate (samples/second)

    damp = 0.015
    gain = 1
    w = 1
    f = 1
    fw_min = 500
    fw_max = 3000
    fw = 2000
    delta = fw / RATE

    


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
    yh = [0.0 for n in range(0, 2*BLOCKSIZE)]
    yb = [0.0 for n in range(0, 2*BLOCKSIZE)]
    yl = [0.0 for n in range(0, 2*BLOCKSIZE)]

    output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]



    # Create a buffer (delay line) for past values
    # buffer_MAX =  1024                          # Buffer length
    buffer = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero
    # buffer2 = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero

    # Buffer (delay line) indices
    kr = 0  # read index
    kw = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
    kw = BLOCKSIZE/2



    output_all = ''            # output signal in all (string)


    # Initialize angle
    theta = 0.0
    # theta2 = 0.0

    # Block-to-block angle increment
    theta_del = (float(BLOCKSIZE*f)/RATE - math.floor(BLOCKSIZE*f/RATE)) * 2.0 * math.pi
    # theta_del2 = (float(BLOCKSIZE*f1)/RATE - math.floor(BLOCKSIZE*f1/RATE)) * 2.0 * math.pi

    num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)
    print ('* Playing...')

    # Loop through wave file 
    for i in range(0, num_blocks):
        # Get sample from wave file
        input_string = stream.read(BLOCKSIZE)

        # Convert string to number
        input_value = struct.unpack('hh'* BLOCKSIZE, input_string)
        fc = fw_min
        f1 = 2 * math.sin(math.pi*fc/RATE)

        # yh = [0.0 for n in range(0, 2*BLOCKSIZE)]
        # yb = [0.0 for n in range(0, 2*BLOCKSIZE)]
        # yl = [0.0 for n in range(0, 2*BLOCKSIZE)]

        # yh[0] = input_value[0]
       	# yb[0] = f1 * yh[0]
       	# yl[0] = f1 * yb[0]
        # Get previous and next buffer values (since kr is fractional)
        # fc = fw_min
        if fc >= fw_max:
            delta = -delta
        if fc <= fw_min:
            delta = -delta
        # Go through block
        for n in range(0, BLOCKSIZE):

        	# if fc >= fw_max:
        	# 	delta = -delta
        	# if fc <= fw_min:
        	# 	delta = -delta

        	f1 = 2 * math.sin(math.pi*fc/RATE)
        	Q1 = 2 * damp

        	yh[2*n] = 1.2*input_value[2*n] - yl[2*(n-1)] - Q1 * yb[2*(n-1)]
        	yb[2*n] = f1 * yh[2*n] + yb[2*(n-1)]
        	yl[2*n] = f1 * yb[2*n] + yl[2*(n-1)]

        	fc = fc + delta
        	yb[2*n] = clip16(yb[2*n])
        	yb[2*n+1] = clip16(yb[2*n])




        output_string = struct.pack('hh'* BLOCKSIZE , *yb)

        # Write output to audio stream
        stream.write(output_string)



        output_all = output_all + output_string


    print('* Done')

    stream.stop_stream()
    stream.close()
    p.terminate()


wah_effect()


# flanger(1,1)
