##################################################
# thread basics: start 10 copies of a function
# running in parallel; uses time.sleep so that 
# main thread doesn't die too early--this kills 
# all other threads on both Windows and Linux;
# stdout shared: thread outputs may be intermixed
##################################################

import thread

def counter(myId, count):
    # this function runs in threads
    for i in range(count): print '[%s] => %s' % (myId, i)

# spawn 10 threads
for i in range(10):
    print thread.start_new(counter, (i, 100))

import time
time.sleep(3) 
print 'Main thread exiting.'  
