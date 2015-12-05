# forks child processes until you type 'q'

import os

def child():
    print 'Hello from child',  os.getpid()
    os._exit(0)  # else goes back to parent loop

def parent():
    while 1:
        newpid = os.fork()
        if newpid == 0:
            child()
        else:
            print 'Hello from parent', os.getpid(), newpid
        if raw_input() == 'q': break

parent()
