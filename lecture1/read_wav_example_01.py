
import wave

# help(wave)

# https://docs.python.org/2/library/wave.html



wf = wave.open('cat01.wav')

print ('number of channels: ', wf.getnchannels())
print ('framerate: ', wf.getframerate())
print ('signal length: ', wf.getnframes())
print ('bytes per frame:', wf.getsampwidth())

wf.close()



wf = wave.open('arctic_a0001.wav')

print ('number of channels: ', wf.getnchannels())
print ('framerate: ', wf.getframerate())
print ('signal length: ', wf.getnframes())
print ('bytes per frame:', wf.getsampwidth())

wf.close()

