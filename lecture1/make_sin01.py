# Make a wave file (.wav) consisting of a sine wave
# Adapted from http://www.swharden.com/blog/2011-07-08-create-mono-and-stereo-wave-files-with-python/

# For 'wave' functions, see:
# https://docs.python.org/2/library/wave.html

# For 'pack' function see:
# https://docs.python.org/2/library/struct.html

from struct import pack
from math import sin, pi
import wave
import random

Fs = 8000

## CREATE MONO FILE ##

wf = wave.open('sin01_mono.wav', 'w')		# wf : wave file
wf.setnchannels(1)			# one channel (mono)
wf.setsampwidth(2)			# two bytes per sample
wf.setframerate(Fs)			# samples per second
maxAmp = 2**15 - 1.0 		# maximum amplitude
f = 261.625565  			# Hz (middle C)
for n in range(0, 1*Fs):	# 1 second duration
	wvData = pack('h', maxAmp * sin(n*2*pi*f/Fs)) 
	# 'h' indicates 'short'
	wf.writeframes(wvData)
wf.close()

## GENERATE STERIO FILE ##

wf = wave.open('sin01_stereo.wav', 'w')
wf.setnchannels(2)			# two channels (stereo)
wf.setsampwidth(2)			# two bytes per sample
wf.setframerate(Fs)			# samples per second
maxAmp = 2**15-1.0 			# maximum amplitude
f1 = 261.625565  			# 261.625565 Hz (middle C)
f2 = 440.0  				# note A4
for n in range(0, 1*Fs):	# 1 second duration
	wvData = pack('h', maxAmp * sin(n*2*pi*f1/Fs)) # left
	wvData += pack('h', maxAmp * sin(n*2*pi*f2/Fs)) # right
	# 'h' indicates 'short'
	wf.writeframes(wvData)
wf.close()
