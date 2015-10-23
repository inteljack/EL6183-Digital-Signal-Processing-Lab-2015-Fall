# feedbackdelay_circbuffer1.py
# Reads a specified wave file (mono) and plays it with a delay with feedback.
# This implementation uses a circular buffer (of minimum
# length) and one buffer index.

import pyaudio
import wave
import struct
import math
from clipping import clip16

wavfile = "drum.wav"
print("Play the wave file %s." % wavfile)

# Open the wave file
wf = wave.open( wavfile, 'rb')

# Read the wave file properties
num_channels = wf.getnchannels()        # Number of channels
Fs = wf.getframerate()                  # Sampling rate (frames/second)
signal_length  = wf.getnframes()        # Signal length
width = wf.getsampwidth()               # Number of bytes per sample

print("The file has %d channel(s)."            % num_channels)
print("The frame rate is %d frames/second."    % Fs)
print("The file has %d frames."                % signal_length)
print("There are %d bytes per sample."         % width)

# Set parameters of delay system
Ga0 = 0.0       #right channel gain a
Ga1 = 0.8       #left channel gain a
Gb0 = 0.5       #right channel gain b
Gb1 = 0.8       #left channel gain b
Gc0 = 0.5       #right channel gain c
Gc1 = 0.8       #left channel gain c

delay_sec0 = 0.8 # 50 milliseconds (should not be zero)
delay_sec1 = 0.5 # 50 milliseconds (should not be zero)
delay_samples0 = int( math.floor( Fs * delay_sec0 ) ) 
delay_samples1 = int( math.floor( Fs * delay_sec1 ) )

print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec0, delay_samples0))

# Create a delay line (buffer) to store past values. Initialize to zero.
buffer_length0 = delay_samples0
buffer_length1 = delay_samples1

echoleft = max(delay_samples0, delay_samples1)
buffer0 = [ 0 for i in range(buffer_length0) ] 
buffer1 = [ 0 for i in range(buffer_length1) ]

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 2,
                rate        = Fs,
                input       = False,
                output      = True )

# Get first frame (sample)
input_string = wf.readframes(1)

# Delay line (buffer) index
k = 0
m = 0

counter0 = 10
counter1 = 10

#initialization
buffer0[k] = 0.0
buffer1[m] = 0.0

print ("**** Playing ****")

while input_string != '':

    # Convert string to numbers
    input_tuple = struct.unpack('hh', input_string)  # produces a two-element tuple

    output_value0 = input_tuple[0] + Gc0 * buffer0[k]
    output_value1 = input_tuple[1] + Gc1 * buffer1[m]

    buffer0[k] = Ga0 * input_tuple[0] + Gb0 * (output_value1 - input_tuple[1])
    buffer1[m] = Ga1 * input_tuple[1] + Gb1 * (output_value0 - input_tuple[0])

    # Increment buffer index
    k = k + 1
    if k == buffer_length0:
        # We have reached the end of the buffer. Circle back to front.
        k = 0

    m = m + 1
    if m == buffer_length1:
        # We have reached the end of the buffer. Circle back to front.
        m= 0

    # Clip output value to 16 bits and convert to binary string
    output_value0 = clip16(output_value0)
    output_value1 = clip16(output_value1)
    output_string = struct.pack('hh', output_value0, output_value1)

    # Write output value to audio stream
    stream.write(output_string)

    # Get next frame (sample)
    input_string = wf.readframes(1) 

while echoleft != 0 and (counter0 > 0 or counter1 > 0) :
    
    output_value0 = Gc0 * buffer0[k]
    output_value1 = Gc1 * buffer1[m]

    buffer0[k] = Gb0 * output_value1
    buffer1[m] = Gb1 * output_value0

    # Increment buffer index
    k = k + 1
    if k == buffer_length0:
        # We have reached the end of the buffer. Circle back to front.
        k = 0
        counter0 = counter0 - 1

    m = m + 1
    if m == buffer_length1:
        # We have reached the end of the buffer. Circle back to front.
        m = 0
        counter1 = counter1 - 1
    
    # Clip output value to 16 bits and convert to binary string
    output_value0 = clip16(output_value0)
    output_value1 = clip16(output_value1)
    output_string = struct.pack('hh', output_value0, output_value1)

    # Write output value to audio stream
    stream.write(output_string)


print("**** Done ****")

stream.stop_stream()
stream.close()
p.terminate()
