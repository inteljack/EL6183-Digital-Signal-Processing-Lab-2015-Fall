
import wave

# help(wave)

# https://docs.python.org/2/library/wave.html

def readsamplewav(filename):
    wf = wave.open(filename)

    print 'number of channels: ', wf.getnchannels()
    print 'framerate: ', wf.getframerate()
    print 'signal length: ', wf.getnframes()
    print 'bytes per frame:', wf.getsampwidth()

    wf.close()

filename = "sample_8bit.wav"
print '8bit'
readsamplewav(filename)
filename = "sample_32bit.wav"
print '32bit'
readsamplewav(filename)
