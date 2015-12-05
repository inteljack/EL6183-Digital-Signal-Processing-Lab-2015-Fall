##########################################################
# catch signals in Python;  pass signal number N as a
# command-line arg, use a "kill -N pid" shell command
# to send this process a signal;  most signal handlers 
# restored by Python after caught (see network scripting
# chapter for SIGCHLD details); signal module avaiable
# on Windows, but defines only a few signal types there; 
##########################################################

import sys, signal, time
def now(): return time.ctime(time.time())        # current time string

def onSignal(signum, stackframe):                # python signal handler
    print 'Got signal', signum, 'at', now()      # most handlers stay in effect

signum = int(sys.argv[1])
signal.signal(signum, onSignal)                  # install signal handler
while 1: signal.pause()                          # wait for signals (or: pass)
