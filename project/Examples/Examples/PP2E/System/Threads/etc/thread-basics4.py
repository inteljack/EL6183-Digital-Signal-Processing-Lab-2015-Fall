import thread

def counter(myId, count):
    # synchronize stdout access to avoid multiple prints on 1 line
    for i in range(count): 
        mutex.acquire()
        print '[%s] => %s' % (myId, i)
        mutex.release()

mutex = thread.allocate_lock()
for i in range(10):
    thread.start_new(counter, (i, 100))

import time
time.sleep(10) 
print 'Main thread exiting.'
