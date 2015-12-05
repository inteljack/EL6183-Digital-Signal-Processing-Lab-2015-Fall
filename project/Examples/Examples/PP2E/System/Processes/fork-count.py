############################################################
# fork basics: start 10 copies of this program running in 
# parallel with the original; each copy counts up to 10
# on the same stdout stream--forks copy process memory, 
# including file descriptors; fork doesn't currently work 
# on Windows: use os.spawnv to start programs on Windows 
# instead; spawnv is roughly like a fork+exec combination;
############################################################

import os, time

def counter(count):
    for i in range(count): 
        time.sleep(1)
        print '[%s] => %s' % (os.getpid(), i)

for i in range(10):
    pid = os.fork()
    if pid != 0:
        print 'Process %d spawned' % pid
    else:
        counter(10)
        os._exit(0)

print 'Main process exiting.'
