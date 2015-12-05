#########################################################
# named pipes; os.mkfifo not avaiable on Windows 95/98;
# no reason to fork here, since fifo file pipes are 
# external to processes--shared fds are irrelevent;
#########################################################

import os, time, sys
fifoname = '/tmp/pipefifo'                       # must open same name

def child():
    pipeout = os.open(fifoname, os.O_WRONLY)     # open fifo pipe file as fd
    zzz = 0 
    while 1:
        time.sleep(zzz)
        os.write(pipeout, 'Spam %03d\n' % zzz)
        zzz = (zzz+1) % 5
         
def parent():
    pipein = open(fifoname, 'r')                 # open fifo as stdio object
    while 1:
        line = pipein.readline()[:-1]            # blocks until data sent
        print 'Parent %d got "%s" at %s' % (os.getpid(), line, time.time())

if __name__ == '__main__':
    if not os.path.exists(fifoname):
        os.mkfifo(fifoname)                      # create a named pipe file
    if len(sys.argv) == 1:
        parent()                                 # run as parent if no args
    else:                                        # else run as child process
        child()
