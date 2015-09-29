# play_delay_longbuffer.py
# Reads a specified wave file (mono) and plays it with a delay and direct path.
# This implementation uses a circular buffer with two buffer indices.
# The buffer is not minimum-length.

import pyaudio
import wave
import struct
import math
from myfunctions import clip16

wavfile = 'author.wav'
print 'Play the wave file: {0:s}.'.format(wavfile)

# Open wave file
wf = wave.open( wavfile, 'rb')

# Read wave file properties
CHANNELS = wf.getnchannels()        # Number of channels
RATE = wf.getframerate()            # Sampling rate (frames/second)
LEN  = wf.getnframes()              # Signal length
WIDTH = wf.getsampwidth()           # Number of bytes per sample

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)

# Delay parameters
Gdp = 0.8           # direct-path gain
Gff = 1.0           # feed-forward gain

delay_sec = 0.05 # 50 milliseconds
# delay_sec = 0.2
delay_samples = int( math.floor( RATE * delay_sec ) ) 

# Create a buffer (delay line) for past values. Initialize to zero.
buffer_MAX =  2048      # Set buffer length.  Must be more than delay_samples!
buffer = [ 0.0 for i in range(buffer_MAX) ]   

# Buffer (delay line) indices
kr = 0              # read index
kw = delay_samples  # write index

print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print 'The buffer is {0:d} samples long.'.format(buffer_MAX)

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = RATE,
                input       = False,
                output      = True )

print ('* Playing...')

# Loop through wave file 
for n in range(0, LEN):

    # Get sample from wave file
    input_string = wf.readframes(1)

    # Convert string to number
    input_value = struct.unpack('h', input_string)[0]

    # Compute output value
    output_value = Gdp * input_value + Gff * buffer[kr]

    # Update buffer (pure delay)
    buffer[kw] = input_value

    # Increment read index
    kr = kr + 1
    if kr == buffer_MAX:
        # End of buffer. Circle back to front.
        kr = 0

    # Increment write index    
    kw = kw + 1
    if kw == buffer_MAX:
        # End of buffer. Circle back to front.
        kw = 0

    # Clip and convert output value to binary string
    output_string = struct.pack('h', clip16(output_value))

    # Write output to audio stream
    stream.write(output_string)

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()
