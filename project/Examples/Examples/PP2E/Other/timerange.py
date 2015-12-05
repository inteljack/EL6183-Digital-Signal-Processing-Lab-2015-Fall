reps = 2000
size = 5000
import time

print 'range...\t',
start = time.time()
for i in range(reps): 
    for i in range(size): pass
stop = time.time()
print stop - start

print 'xrange...\t',
start = time.time()
for i in range(reps): 
    for i in xrange(size): pass
stop = time.time()
print stop - start

raw_input('Press enter')
