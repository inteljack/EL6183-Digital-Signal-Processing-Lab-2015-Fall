############################################################
# do something simlar by forking process instead of threads
# this doesn't currently work on Windows, because it has no
# os.fork call; use os.spawnv to start programs on Windows 
# instead; spawnv is roughly like a fork+exec combination;
############################################################

import os, sys

def counter(count):
    for i in range(count): print '[%s] => %s' % (os.getpid(), i)

for i in range(10):
    pid = os.fork()
    if pid != 0:
        print 'Process %d spawned' % pid
    else:
        counter(100)
        sys.exit()

print 'Main process exiting.'
