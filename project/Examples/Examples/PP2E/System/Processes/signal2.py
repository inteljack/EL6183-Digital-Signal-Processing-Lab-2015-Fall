##########################################################
# set and catch alarm timeout signals in Python; 
# time.sleep doesn't play well with alarm (or signal
# in general in my Linux PC), so call signal.pause 
# here to do nothing until a signal is received;
##########################################################

import sys, signal, time
def now(): return time.ctime(time.time())

def onSignal(signum, stackframe):                # python signal handler
    print 'Got alarm', signum, 'at', now()       # most handlers stay in effect

while 1:
    print 'Setting at', now()
    signal.signal(signal.SIGALRM, onSignal)      # install signal handler
    signal.alarm(5)                              # do signal in 5 seconds
    signal.pause()                               # wait for signals
