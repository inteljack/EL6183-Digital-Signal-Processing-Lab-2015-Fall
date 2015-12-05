# same as pipe1.py, but wrap pipe input in stdio file object
# to read by line, and close unused pipe fds in both processes

import os, time

def child(pipeout):
    zzz = 0
    while 1:
        time.sleep(zzz)                          # make parent wait
        os.write(pipeout, 'Spam %03d\n' % zzz)   # send to parent
        zzz = (zzz+1) % 5                        # roll to 0 at 5
         
def parent():
    pipein, pipeout = os.pipe()                  # make 2-ended pipe
    if os.fork() == 0:                           # in child, write to pipe
        os.close(pipein)                         # close input side here
        child(pipeout)
    else:                                        # in parent, listen to pipe
        os.close(pipeout)                        # close output side here
        pipein = os.fdopen(pipein)               # make stdio input object
        while 1:
            line = pipein.readline()[:-1]        # blocks until data sent
            print 'Parent %d got "%s" at %s' % (os.getpid(), line, time.time())

parent()
