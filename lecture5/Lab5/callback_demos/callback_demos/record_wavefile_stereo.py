# record_wavefile_stereo.py 
# Record stereo audio to a wave file using callback 

import pyaudio
import wave
import time
import struct
from myfunctions import clip16

filename = 'test_stereo.wav'

RATE = 16000    # sampling rate
CHANNELS = 2    # stereo
WIDTH = 2       # bytes of each sample
gain_L = 1.0    # gain for amplifying (Left)
gain_R = 0.4    # gain for amplifying (Right)

counter = 1

# Define callback function for recording audio
def my_callback(input_string, block_size, time_info, status):
    global counter
    if counter > 0:
        print 'block size is',block_size
        print 'time info is',time_info
        print 'status is', status
        counter = counter -1
    input_frame = struct.unpack('hh', input_string)

    sample_left = clip16( gain_L * input_frame[0] )
    sample_right = clip16( gain_R * input_frame[1] )

    # output_data.append(sample_left)
    # output_data.append(sample_right)

    # OR use 'extend' method
    output_frame = [sample_left, sample_right]
    output_data.extend(output_frame)
    
    return (input_string, pyaudio.paContinue)

p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = False,
                frames_per_buffer = 1,
                stream_callback = my_callback)

output_data = []

stream.start_stream()
print '* Recording 4 seconds ...'

time.sleep(4.0)

stream.stop_stream()
print 'Done.'

# Close audio stream
stream.close()
p.terminate()

# Convert output signal to binary string
output_string = struct.pack('h'*len(output_data), *output_data)

# Write data to wave file
wf = wave.open(filename, 'w')
wf.setnchannels(CHANNELS)
wf.setsampwidth(WIDTH)
wf.setframerate(RATE)
wf.writeframes(output_string)
wf.close()
