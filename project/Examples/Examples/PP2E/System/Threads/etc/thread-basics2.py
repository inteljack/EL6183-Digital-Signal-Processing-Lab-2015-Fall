import thread, time

def counter(myId, count):
    for i in range(count): 
        time.sleep(1)
        print 'thread number %d reporting in at %d...' % (myId, time.clock())

# 5 threads, each sleeps 3 second in parallel
# total time for all threads is roughly 3 seconds
# time.clock(): seconds since last clock() call

print time.clock()
for i in range(5):
    thread.start_new(counter, (i, 3))

time.sleep(5) 
print 'Main thread exiting.'
