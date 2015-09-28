# play_wav_mono.py

import pyaudio
import wave
import struct
import math
import sys
import clipping


gain = 0.5

# wavfile = 'author.wav'
wavfile = sys.argv[1]
# wavfile = 'sin01_stereo.wav'

bitformat = sys.argv[2]
bitformat = int(bitformat)

print("Play the wave file %s in %d bit per sample." % (wavfile,bitformat))

wf = wave.open( wavfile, 'rb' )

# Read the wave file properties
num_channels = wf.getnchannels()        # Number of channels
Fs = wf.getframerate()                  # Sampling rate (frames/second)
signal_length  = wf.getnframes()        # Signal length
width = wf.getsampwidth()               # Number of bytes per sample

print("The file has %d channel(s)."            % num_channels)
print("The frame rate is %d frames/second."    % Fs)
print("The file has %d frames."                % signal_length)
print("There are %d bytes per sample."         % width)

p = pyaudio.PyAudio()

stream = p.open(format      = pyaudio.paInt16,
                channels    = num_channels,
                rate        = Fs,
                input       = False,
                output      = True )

input_string = wf.readframes(1)          # Get first frame

if num_channels == 1:
    while input_string != '':

        if bitformat == 16:
            # Convert string to number
            input_tuple = struct.unpack('h', input_string)  # One-element tuple
            input_value = input_tuple[0]                    # Number

            # Compute output value
            output_value = clipping.clip16(gain * input_value)    # Number

            # Convert output value to binary string
            output_string = struct.pack('h', output_value) 

        elif bitformat == 32:
            input_tuple = struct.unpack('f', input_string)  # One-element tuple
            input_value = input_tuple[0]                    # Number
            output_value = clipping.clip32(gain * input_value)    # Number
            output_string = struct.pack('f', output_value)  # Convert output value to binary string
        # Write output value to audio stream
        stream.write(output_string)

        # Get next frame
        input_string = wf.readframes(1)
elif num_channels == 2:
    while input_string != '':
        if bitformat == 16:
            # Convert string to numbers
            input_tuple = struct.unpack('hh',input_string)  # produces a two-element tuple

            # Compute output values
            output_value0 = clipping.clip16(gain * input_tuple[0])
            output_value1 = clipping.clip16(gain * input_tuple[1])

            # Convert output value to binary string
            output_string = struct.pack('hh', output_value0, output_value1)
        
        elif bitformat == 32:
            input_tuple = struct.unpack('hh', input_string)  # produces a two-element tuple
            output_value0 = clipping.clip32(gain * input_tuple[0])
            output_value1 = clipping.clip32(gain * input_tuple[1])
            output_string = struct.pack('ii', output_value0, output_value1)
        # Write output value to audio stream
        stream.write(output_string)

        # Get next frame
        input_string = wf.readframes(1)
else:
    print("**** File format not support *****")
    
print("**** Done ****")

stream.stop_stream()
stream.close()
p.terminate()
