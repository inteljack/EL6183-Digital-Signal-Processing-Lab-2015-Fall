# record_wavefile.py
# Record audio to a wave file using callback 

import pyaudio
import wave
import time
import struct
from myfunctions import clip16

filename = 'test_01.wav'		# Output wave file

CHANNELS = 1
RATE = 16000
WIDTH = 2
GAIN = 1.0

def my_callback_fun(input_string, block_size, time_info, status):
    input_tuple = struct.unpack('h', input_string)
    output_sample = clip16(GAIN * input_tuple[0])
    output_list.append(output_sample)
    return (input_string, pyaudio.paContinue)

p = pyaudio.PyAudio()

# Set PyAudio format
PA_format = p.get_format_from_width(WIDTH)

stream = p.open(format = PA_format,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = False,
                frames_per_buffer = 1,
                stream_callback = my_callback_fun)

output_list = []

stream.start_stream()
print '* Start Recording *'

time.sleep(4.0)

stream.stop_stream()
print '* Finish Recording *'

stream.close()
p.terminate()

# Convert output signal to binary signal to write to wave file 
output_string = struct.pack('h'*len(output_list), *output_list)

# write data into wav file
wf = wave.open(filename, 'w')
wf.setnchannels(CHANNELS)
wf.setsampwidth(WIDTH)
wf.setframerate(RATE)
wf.writeframes(output_string)
wf.close()

