import thread, time, sys
sys.setcheckinterval(20)
count = 0

def adder():
    global count 
    count = count + 1         # update shared global 
    count = count + 1         # thread swapped out before returns

for i in range(100): 
    thread.start_new(adder, ())    # start 100 update threads
time.sleep(5)
print count
