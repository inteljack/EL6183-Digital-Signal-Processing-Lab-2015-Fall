# uses higher-level java like threading module object
# join method (not mutexes or shared global vars) to  
# know when threads are done in parent/main thread;
# see library manual for more details on threading;
# note that this scheme sometimes doesn't multiplex
# the threads as evenly on Windows as simple thread
# module--some run to completion before others run;

import threading, thread

class mythread(threading.Thread):          # subclass Thread object
    def __init__(self, myId, count):
        self.myId  = myId
        self.count = count
        threading.Thread.__init__(self)   
    def run(self):                         # run provides thread logic
        for i in range(self.count):        # still synch stdout access
            stdoutmutex.acquire()
            print '[%s] => %s' % (self.myId, i)
            stdoutmutex.release()

stdoutmutex = thread.allocate_lock()
threads = []
for i in range(10):
    thread = mythread(i, 100)             # make/start 10 threads
    thread.start()                        # start run method in a thread
    threads.append(thread) 

for thread in threads:
    thread.join()                         # wait for thread exits
print 'Main thread exiting.'
