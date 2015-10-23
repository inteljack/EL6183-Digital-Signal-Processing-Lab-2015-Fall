# plot_micinput_ver.py
"""
Using Pyaudio, record sound from the audio device and plot,
for 8 seconds, and display it live in a Window.
Usage example: python pyrecplotanimation.py
Gerald Schuller, October 2014 
Modified: Ivan Selesnick, September 2015
"""

import pyaudio
import struct
import numpy as np
import math
from matplotlib import pyplot as plt
from myfunctions import clip16
import sys    
import os

file_name =  os.path.basename(sys.argv[0])

plt.ion()           # Turn on interactive mode so plot gets updated

WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
RATE = 48000        # Sampling rate (samples/second)
BLOCKSIZE = 1024
DURATION = 1       # Duration in seconds


print 'BLOCKSIZE =', BLOCKSIZE
print 'Running for ', DURATION, 'seconds...'

# Initialize plot window:
fig = plt.figure(1)
plt.ylim(-20000,20000)        # set y-axis limits
# plt.ylabel('dB')

plt.xlim(0, BLOCKSIZE)         # set x-axis limits
plt.xlabel('Time (n)')

t = range(0, BLOCKSIZE)
capture = [0.0 for i in range(0,BLOCKSIZE)]

# # Time axis in units of milliseconds:
# plt.xlim(0, 1000.0*BLOCKSIZE/RATE)         # set x-axis limits
# plt.xlabel('Time (msec)')
# t = [n*1000/float(RATE) for n in range(BLOCKSIZE)]

line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(t)                         # x-data of plot (time)

# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = False)

output_file = file_name[:-3] + '_room_response.pdf'
flag = 0
start = 0

while(flag != 1):
	input_string = stream.read(BLOCKSIZE)                     # Read audio input stream
	input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)  # Convert
	
	for n in range(0, BLOCKSIZE):
		if abs(input_tuple[n]) > 300:
			print input_tuple[n]
			start = n
			for j in range(0,BLOCKSIZE-start):
				capture[j] = input_tuple[j+start]
			flag = 1
			break
	line.set_ydata(input_tuple)                               # Update y-data of plot
	plt.draw()

input_string = stream.read(BLOCKSIZE)                     # Read audio input stream
input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)  # Convert

for j in range(0,BLOCKSIZE-start-1):
	capture[start+j+1] = input_tuple[j]


	# X = np.fft.fft(input_tuple)
	# dB = 20* np.log10(abs(X))
	# print 'dB =', np.max(dB)
line.set_ydata(input_tuple)                               # Update y-data of plot
plt.draw()
	
	# if np.max(dB) > 120:

	# 	while(flag != 1):
fig.savefig(output_file)
	# 		flag = 1
	# 	break

# for i in range(0, NumBlocks):
#     input_string = stream.read(BLOCKSIZE)                     # Read audio input stream
#     input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)  # Convert
    

# plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print '* Done'
