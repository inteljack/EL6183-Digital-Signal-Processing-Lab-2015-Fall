
import wave

# use a loop:

wav_list = ['cat01.wav', 'arctic_a0001.wav']
for wav_file in wav_list:
	wf = wave.open(wav_file)
	print 'File:', wav_file
	print 'number of channels: ', wf.getnchannels() 
	print 'framerate: ', wf.getframerate(), 'per second'
	print 'signal length: ', wf.getnframes(), 'frames'
	print 'bytes per frame:', wf.getsampwidth() 
	print ''
	wf.close()
	
