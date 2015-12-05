
import pyaudio
import struct
import wave
import numpy as np
from matplotlib import pyplot as plt
import myfunctions
import  scipy.signal as signal
# Open wave file (mono)
# wave_file_name = '1500.wav'
wave_file_name = 'author.wav'
# wave_file_name = '920.wav'

wf = wave.open( wave_file_name, 'rb')
RATE = wf.getframerate()
WIDTH = wf.getsampwidth()
LEN = wf.getnframes() 
CHANNELS = wf.getnchannels() 
BLOCKSIZE = 2**12
f0 = 0              # 'dock audio'
NumBlocks = int(np.floor(LEN/BLOCKSIZE))
I = 1j
print 'Rate =', RATE
print 'Width =', WIDTH
print 'Number of frames =', LEN
print 'Number of channels =', CHANNELS
print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks

t =[n for n in range(0, RATE*2)]

plt.ion()           # Turn on interactive mode so plot gets updated
plt.figure(1)
# plt.subplot(2,1,1)
# plt.ylim(-10, 180)        # set y-axis limits
# plt.xlim(35, 95)         # set x-axis limits
# plt.xlabel('Frequency (n)')
# plt.ylabel('dB')
# line1, = plt.plot([], [], color = 'blue')  # Create empty line
# line1.set_xdata(t)                         # x-data of plot (time)


# plt.subplot(2,1,2)
plt.ylim(0, 50*np.log10(10*RATE))           # set y-axis limits
plt.xlim(0, 5000)          # set x-axis limits
plt.xlabel('Frequency (n)')
plt.ylabel('dB')
line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(t) # x-data of plot (time)



output_block = [0 for n in range(0, BLOCKSIZE)]

fs_Hz = RATE


####################

### make2ndAllpassNotch
## usage: [a,b] = make2ndAllpassNotch(f1,RATE,R)
## where a and b are coefficient sets of the transfer function
def make2ndAllpassNotch(f,fs,R):    
    om = 2.0 * np.pi * float(f)/fs
    a1 = -2 * R * np.cos(om)
    a2 = R**2
    a = [1, a1, a2]
    b = list(a)
    b.reverse()
    return a,b

### make1stAllpassNotch
## usage: [a,b] = make1stAllpassNotch(f1,RATE)
## where a and b are coefficient sets of the transfer function
def makeDelayAllpassNotch(f,fs,delay):  
    om = 2.0 * np.pi * float(f)/fs
    a1 = np.tan(om/2) + 1.0
    a2 = np.tan(om/2) - 1.0
    a = [0 for i in range(delay+1)]
    a[0] = a1
    a[delay] = a2 
    b = list(a)
    b.reverse()
    print 'a2=',a2
    print 'a=',a
    print 'b=',b
    return a,b

# R = 0.9
f1 = 10
# f2 = 500
# [a,b] = make2ndAllpassNotch(f1,RATE,R)
[a,b] = makeDelayAllpassNotch(f1,RATE,10)
# np.convolve(a_apf1,a_apf2)
# H = exp(-I * 10 * np.pi * n / BLOCKSIZE)


####################

# print f[910:930]
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True)

for i in range(0, NumBlocks):
    # Get frames from audio input stream
    input_string = wf.readframes(BLOCKSIZE)       # BLOCKSIZE = number of frames read
    input_tuple = struct.unpack('h' *BLOCKSIZE, input_string)    # Convert

    output_block = signal.filtfilt(b,a,input_tuple)
    # output_block1 = signal.filtfilt(b,a,input_tuple)
    # output_block = signal.filtfilt(b2,a2,output_block1)
    
    for n in range(0, BLOCKSIZE):
        output_block[n] = myfunctions.clip16(np.abs(output_block[n]+input_tuple[n]))
        # output_block[n] = output_block[n] * np.cos(2*np.pi*n*f0/RATE + theta)
    
    # input_block_fft = np.fft.fft(input_tuple,RATE*2)
    output_block_fft = np.fft.fft(output_block,RATE*2)
    
    
    line.set_ydata(np.log10(abs(output_block_fft))*20)
    # line.set_ydata(np.log10(abs(input_block_fft))*20)
    # line.set_ydata(abs(output_block_fft))

    # plt.subplot(2,1,2)
    # line1.set_ydata(np.log10(abs(input_block_fft))*20)
    plt.draw()

    output_string = struct.pack('h' *BLOCKSIZE, *output_block)
    # output_string = struct.pack('hh' * BLOCKSIZE*NumBlocks, *input_tuple)
    stream.write(output_string)

plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print '* Done'

