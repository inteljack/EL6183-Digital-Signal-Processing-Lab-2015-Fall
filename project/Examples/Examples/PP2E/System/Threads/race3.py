import thread, time, sys
mutex = thread.allocate_lock()
count = 0

def adder():
    global count 
    mutex.acquire()
    count = count + 1         # update shared global 
    count = count + 1         # thread swapped out before returns
    mutex.release()

for i in range(100): 
    thread.start_new(adder, ())    # start 100 update threads
time.sleep(5)
print count
