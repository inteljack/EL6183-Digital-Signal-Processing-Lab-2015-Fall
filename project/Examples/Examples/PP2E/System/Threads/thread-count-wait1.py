##################################################
# uses mutexes to know when threads are done
# in parent/main thread, instead of time.sleep;
# lock stdout to avoid multiple prints on 1 line;
##################################################

import thread

def counter(myId, count):
    for i in range(count): 
        stdoutmutex.acquire()
        print '[%s] => %s' % (myId, i)
        stdoutmutex.release()
    exitmutexes[myId].acquire()  # signal main thread

stdoutmutex = thread.allocate_lock()
exitmutexes = []
for i in range(10):
    exitmutexes.append(thread.allocate_lock())
    thread.start_new(counter, (i, 100))

for mutex in exitmutexes:
    while not mutex.locked(): pass
print 'Main thread exiting.'
