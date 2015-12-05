##########################################################
# Demo Python's signal module; pass signal number as a
# command-line arg, use a "kill -N pid" shell command
# to send this process a signal; e.g., on my linux 
# machine, SIGUSR1=10, SIGUSR2=12, SIGCHLD=17, and 
# SIGCHLD handler stays in effect even if not restored:
# all other handlers restored by Python after caught,
# but SIGCHLD is left to the platform's implementation;
# signal works on Windows but defines only a few signal
# types; signals are not very portable in general;
##########################################################

import sys, signal, time

def now():
    return time.ctime(time.time())

def onSignal(signum, stackframe):                # python signal handler
    print 'Got signal', signum, 'at', now()      # most handlers stay in effect
    if signum == signal.SIGCHLD:                 # but sigchld handler is not 
        print 'sigchld caught'
        #signal.signal(signal.SIGCHLD, onSignal)

signum = int(sys.argv[1])
signal.signal(signum, onSignal)                  # install signal handler
while 1: signal.pause()                          # sleep waiting for signals
