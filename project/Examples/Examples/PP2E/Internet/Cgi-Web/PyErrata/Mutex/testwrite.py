#!/usr/bin/python

import os, fcntl, time
from FCNTL import LOCK_EX, LOCK_UN
print os.getpid(), 'start writer', time.time()

file = open('test.lck', 'r')                      # open the lock file
fcntl.flock(file.fileno(), LOCK_EX)               # block if any read or write
print os.getpid(), 'got write lock', time.time()  # only 1 writer at a time

log = open('Shared.txt', 'a')
time.sleep(3)
log.write('%d Hello\n' % os.getpid())

print os.getpid(), 'unlocking\n'
fcntl.flock(file.fileno(), LOCK_UN)               # resume blocked read or write

