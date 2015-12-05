# play_keys.py

"""
PyAudio Example: Generate random pulses and input them to an IIR filter of 2nd order.
Gerald Schuller, March 2015 
Modified - Ivan Selesnick, October 2015
"""

import pyaudio
import struct
import pygame
import numpy as np
from math import sin, cos, pi

BLOCKSIZE = 32      # Number of frames per block
WIDTH = 2           # Bytes per sample
CHANNELS = 1        # Mono
RATE = 16000        # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 1.2    # Decay time (seconds)
f1 = 320    # Frequency (Hz)

# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
om1 = 2.0 * pi * float(f1)/RATE

# Filter coefficients (second-order IIR)
a1 = -2*r*cos(om1)
a2 = r**2
b0 = sin(om1)

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                frames_per_buffer = BLOCKSIZE,  # Make small to avoid latency...
                rate = RATE,
                input = False,
                output = True)

pygame.init()  # Initializes pygame

print "Press keys for sound. Press 'q' to quit."
print "OK go..."

y = np.zeros(BLOCKSIZE)
x = np.zeros(BLOCKSIZE)

stop = False

while stop == False:

    x[0] = 0.0

    for event in pygame.event.get():
    
        # Any key press counts as playing a note
        if event.type == pygame.KEYDOWN:
            x[0] = 15000

        # Quit if user presses 'q'
        if event.key == pygame.K_q:
            stop = True

    # Do difference equation for block
    for n in range(BLOCKSIZE):
        y[n] = b0 * x[n] - a1 * y[n-1] - a2 * y[n-2]  
        # What happens when n = 0?
        # In Python negative indices cycle to end, so it works..

    y = np.clip(y, -MAXVALUE, MAXVALUE)     # Clipping

    # Convert numeric list to binary string
    data = struct.pack('h' * BLOCKSIZE, *y);

    # Write binary string to audio output stream
    stream.write(data, BLOCKSIZE)

print 'Done.'

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()

pygame.quit()
