
import pyaudio
import struct
import wave
import math
import cmath
import numpy as np
from matplotlib import pyplot as plt
import myfunctions
import  scipy.signal as signal
# Open wave file (mono)
# wave_file_name = '1500.wav'
wave_file_name = 'sin_440Hz_stereo.wav'
# wave_file_name = '920.wav'

wf = wave.open( wave_file_name, 'rb')
RATE = wf.getframerate()
WIDTH = wf.getsampwidth()
LEN = wf.getnframes() 
CHANNELS = wf.getnchannels() 
BLOCKSIZE = 512
f0 = 0              # 'dock audio'
NumBlocks = int(math.floor(LEN/BLOCKSIZE))
I = cmath.sqrt(-1)

print 'Rate =', RATE
print 'Width =', WIDTH
print 'Number of frames =', LEN
print 'Number of channels =', CHANNELS
print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks

plt.ion()           # Turn on interactive mode so plot gets updated
plt.figure(1)


filter_order = 2    # 4 order filte

t =[n for n in range(0, RATE*2)]

output_block = [0 for n in range(0, BLOCKSIZE*NumBlocks)]

# N, Wn = signal.buttord([10, 500], [50, 70], 3, 40, True)
fs_Hz = RATE

# create the 60 Hz filter
# bp_stop_Hz = np.array([538.0, 542.0])
bp_stop_Hz = np.array([538.0, 642.0])
b, a = signal.butter(filter_order,bp_stop_Hz/(fs_Hz / 2.0), 'bandstop')
# print b
# print a
# create the 50 Hz filter
# bp2_stop_Hz = np.array([578, 582.0])
bp2_stop_Hz = np.array([678, 782.0])
b2, a2 = signal.butter(2,bp2_stop_Hz/(fs_Hz / 2.0), 'bandstop')

# compute the frequency response
w, h = signal.freqz(b,a,RATE)
# w, h2 = signal.freqz(b2,a2,1000)
f = w * fs_Hz / (2*np.pi)             

# print f[910:930]
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True)



input_string = wf.readframes(BLOCKSIZE*NumBlocks)                     # Read audio input stream
input_tuple = struct.unpack('h'*BLOCKSIZE*NumBlocks, input_string)    # Convert

output_block1 = signal.filtfilt(b,a,input_tuple)
output_block = signal.filtfilt(b2,a2,output_block1)

input_block_fft = np.fft.fft(input_tuple,RATE*2)
output_block_fft = np.fft.fft(output_block,RATE*2)

plt.subplot(2,1,1)
plt.ylim(-10, 180)        # set y-axis limits
plt.xlim(35, 95)         # set x-axis limits
plt.xlabel('Frequency (n)')
plt.ylabel('dB')
line1, = plt.plot([], [], color = 'blue')  # Create empty line
line1.set_xdata(t)                         # x-data of plot (time)
line1.set_ydata(np.log10(abs(input_block_fft))*20)

plt.subplot(2,1,2)
plt.ylim(-10, 180)        # set y-axis limits
plt.xlim(35, 95)         # set x-axis limits
plt.xlabel('Frequency (n)')
plt.ylabel('dB')
line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(t) 
line.set_ydata(np.log10(abs(output_block_fft))*20)
                        # x-data of plot (time)

plt.draw()

for n in range(0,BLOCKSIZE*NumBlocks):
    output_block[n] = myfunctions.clip16(np.real(output_block[n]))

output_string = struct.pack('h' * BLOCKSIZE*NumBlocks, *output_block)
# output_string = struct.pack('hh' * BLOCKSIZE*NumBlocks, *input_tuple)
stream.write(output_string)

plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print '* Done'
















