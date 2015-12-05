#!/usr/local/bin/python

import os, sys                            # unix, python services 
from posixpath import exists              # file exists test
from time import time, ctime              # time functions

if len(sys.argv) != 4:
    print 'use: batch <program> <input> <output>'
    sys.exit(1)

print 'batch run start.' 
print 'what: ', sys.argv[1]
print 'who:  ', os.environ['USER']        # environment variables
print 'where:', os.getcwd()               # directory
print 'when: ', ctime(time())

if exists(sys.argv[3]):
    os.rename(sys.argv[3], sys.argv[3] + '.bkp')       # backup output

os.system('%s < %s > %s 2>&1' % tuple(sys.argv[1:]))   # run command
print 'batch run done.'
