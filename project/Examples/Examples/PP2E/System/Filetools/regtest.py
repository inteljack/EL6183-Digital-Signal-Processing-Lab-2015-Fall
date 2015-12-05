#!/usr/local/bin/python
import os, sys                            # get unix, python services 
from stat import ST_SIZE                  # or use os.path.getsize
from glob import glob                     # file-name expansion
from os.path import exists                # file exists test
from time import time, ctime              # time functions

print 'RegTest start.' 
print 'user:', os.environ['USER']         # environment variables
print 'path:', os.getcwd()                # current directory
print 'time:', ctime(time()), '\n'
program = sys.argv[1]                     # two command-line args
testdir = sys.argv[2]

for test in glob(testdir + '/*.in'):      # for all matching input files
    if not exists('%s.out' % test):
        # no prior results
        os.system('%s < %s > %s.out 2>&1' % (program, test, test))
        print 'GENERATED:', test
    else: 
        # backup, run, compare
        os.rename(test + '.out', test + '.out.bkp')
        os.system('%s < %s > %s.out 2>&1' % (program, test, test))
        os.system('diff %s.out %s.out.bkp > %s.diffs' % ((test,)*3) )
        if os.stat(test + '.diffs')[ST_SIZE] == 0:
            print 'PASSED:', test 
            os.remove(test + '.diffs')
        else:
            print 'FAILED:', test, '(see %s.diffs)' % test

print 'RegTest done:', ctime(time())
