# tapped_delay_line.py
# Reads a specified wave file (mono) and plays it with a tapped_delay_line with feedback.
# This implementation uses a circular buffer.

import pyaudio
import wave
import struct
import math
from myfunctions import clip16

wavfile = "author.wav"
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
Gfb = 0.5       # feed-back gain
g0 = 0.7        # direct-path gain
g1 = 0.4        # a feed-forward gain
g2 = 0.3        # a feed-forward gain

# Set g0 = Gdp, g1 = 0, g2 = Gff to recover system in feedbackdelay_circbuffer.py
#  (Check..)

delay1_sec = 0.03
delay2_sec = 0.07   # delay2_sec > delay1_sec

delay1 = int( math.floor( Fs * delay1_sec ) )    # Delay in samples
delay2 = int( math.floor( Fs * delay2_sec ) ) 

# Create a delay line (buffer) to store past values. Initialize to zero.
buffer_length = delay2      # minimal-length buffer
buffer = [ 0 for i in range(buffer_length) ]    

print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay1_sec, delay1))
print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay2_sec, delay2))
print('My buffer is of length {0:d}'.format(buffer_length))

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = Fs,
                input       = False,
                output      = True )

# Get first frame (sample)
input_string = wf.readframes(1)

# Delay line (buffer) indices
k = 0
m1 = delay1
m2 = 0

print ("**** Playing ****")

while input_string != '':

    # Convert string to number
    input_value = struct.unpack('h', input_string)[0]

    # Compute output value
    output_value = g0 * input_value + g1 * buffer[m1] + g2 * buffer[m2];

    # Update buffer
    buffer[k] = input_value + Gfb * buffer[k]

    # Update buffer indices
    k = k + 1
    m1 = m1 + 1
    m2 = m2 + 1
    if k == buffer_length:
        k = 0
    if m1 >= buffer_length:
        m1 = 0
    if m2 >= buffer_length:
        m2 = 0

    # Clip output value and convert to binary string
    output_string = struct.pack('h', clip16(output_value))

    # Write output value to audio stream
    stream.write(output_string)

    # Get next frame (sample)
    input_string = wf.readframes(1)     

print("**** Done ****")

stream.stop_stream()
stream.close()
p.terminate()
