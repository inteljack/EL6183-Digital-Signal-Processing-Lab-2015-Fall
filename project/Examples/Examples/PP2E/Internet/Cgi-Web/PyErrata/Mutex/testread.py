#!/usr/bin/python

import os, fcntl, time
from FCNTL import LOCK_SH, LOCK_UN
print os.getpid(), 'start reader', time.time()

file = open('test.lck', 'r')                     # open the lock file for fd
fcntl.flock(file.fileno(), LOCK_SH)              # block if a writer has lock
print os.getpid(), 'got read lock', time.time()  # any number of readers can run

time.sleep(3)
print 'lines so far:', os.popen('wc -l Shared.txt').read(),

print os.getpid(), 'unlocking\n'
fcntl.flock(file.fileno(), LOCK_UN)              # resume blocked writers now 

