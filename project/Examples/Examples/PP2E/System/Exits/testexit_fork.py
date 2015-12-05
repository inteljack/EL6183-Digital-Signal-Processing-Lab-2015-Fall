############################################################
# fork child processes to watch exit status with os.wait;
# fork works on Linux but not Windows as of Python 1.5.2;
# note: spawned threads share globals, but each forked 
# process has its own copy of them--exitstat always the 
# same here but will vary if we start threads instead;
############################################################

import os                                   
exitstat = 0 

def child():                                 # could os.exit a script here 
    global exitstat                          # change this process's global
    exitstat = exitstat + 1                  # exit status to parent's wait
    print 'Hello from child', os.getpid(), exitstat
    os._exit(exitstat) 
    print 'never reached'                

def parent():
    while 1:
        newpid = os.fork()                   # start a new copy of process
        if newpid == 0:                      # if in copy, run child logic
            child()                          # loop until 'q' console input
        else:
            pid, status = os.wait()
            print 'Parent got', pid, status, (status >> 8)
            if raw_input() == 'q': break

parent()
