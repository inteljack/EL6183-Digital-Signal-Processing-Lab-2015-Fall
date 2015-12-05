##################################################
# synchronize access to stdout: because it is 
# shared global, thread outputs may be intermixed
##################################################

import thread, time

def counter(myId, count):
    for i in range(count): 
        mutex.acquire()
        #time.sleep(1)
        print '[%s] => %s' % (myId, i)
        mutex.release()

mutex = thread.allocate_lock()
for i in range(10):      
    thread.start_new_thread(counter, (i, 3))

time.sleep(6) 
print 'Main thread exiting.'  
