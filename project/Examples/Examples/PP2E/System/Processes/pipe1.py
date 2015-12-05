import os, time

def child(pipeout):
    zzz = 0
    while 1:
        time.sleep(zzz)                          # make parent wait
        os.write(pipeout, 'Spam %03d' % zzz)     # send to parent
        zzz = (zzz+1) % 5                        # goto 0 after 4
         
def parent():
    pipein, pipeout = os.pipe()                  # make 2-ended pipe
    if os.fork() == 0:                           # copy this process
        child(pipeout)                           # in copy, run child
    else:                                        # in parent, listen to pipe
        while 1:
            line = os.read(pipein, 32)           # blocks until data sent
            print 'Parent %d got "%s" at %s' % (os.getpid(), line, time.time())

parent()
