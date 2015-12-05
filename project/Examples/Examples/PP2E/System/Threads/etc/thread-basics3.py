#########################################################
# also see: threading module's higher-level java-like 
# interfaces;  note: the start_new() call is the same 
# as start_new_thread(); threads work on Windows, IRIX,
# Solaris and systems with pthreads available; threads 
# are liight-weight processes: they run in parallel, 
# but share the same global data space within a process;
#########################################################

import thread, time

def counter(myId, count):
    for i in range(count): 
        mutex.acquire()
        print 'thread number %d reporting in at %d...' % (myId, time.clock())
        time.sleep(1)
        mutex.release()

# 5 threads, each sleeps 1 second at a time;
# here, they are serialized by the mutex lock
# instead of all running in parallel: the threads
# take roughly 15 seconds to complete instead of 3,
# and we get one printed message per second, not 3

print time.clock()
mutex = thread.allocate_lock()
for i in range(5):
    thread.start_new(counter, (i, 3))

time.sleep(20) 
print 'Main thread exiting.'
