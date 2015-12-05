####################################################
# uses simple shared global data (not mutexes) to  
# know when threads are done in parent/main thread;
####################################################

import thread
stdoutmutex = thread.allocate_lock()
exitmutexes = [0] * 10

def counter(myId, count):
    for i in range(count): 
        stdoutmutex.acquire()
        print '[%s] => %s' % (myId, i)
        stdoutmutex.release()
    exitmutexes[myId] = 1  # signal main thread

for i in range(10):
    thread.start_new(counter, (i, 100))

while 0 in exitmutexes: pass
print 'Main thread exiting.'
