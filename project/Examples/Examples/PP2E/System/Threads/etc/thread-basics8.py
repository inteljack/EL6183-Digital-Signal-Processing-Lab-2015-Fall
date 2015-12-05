# uses simple shared global data (not mutexes) to  
# know when threads are done in parent/main thread;

import thread

def counter(myId, count):
    # synchronize stdout access to avoid multiple prints on 1 line
    for i in range(count): 
        stdoutmutex.acquire()
        print '[%s] => %s' % (myId, i)
        stdoutmutex.release()
    exitmutexes[myId] = 1  # signal main thread

stdoutmutex = thread.allocate_lock()
exitmutexes = []
for i in range(10):
    exitmutexes.append(0)
    thread.start_new(counter, (i, 100))

while 0 in exitmutexes: pass
print 'Main thread exiting.'
