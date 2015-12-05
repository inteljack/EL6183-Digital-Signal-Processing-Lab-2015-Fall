#!/usr/local/bin/python

import os, sys                            # unix, python services 
from stat import ST_SIZE                  # C's file stat record 
from glob import glob                     # file-name expansion
from posixpath import exists              # file exists test
from time import time, ctime              # time functions

if len(sys.argv) < 2:
    print 'use: regtest <program> <script-path>?'
    sys.exit(1)
else:
    program = sys.argv[1]

print 'regtest start.' 
print 'user:', os.environ['USER']         # shell: who's running?
print 'path:', os.getcwd()                # where am running?
print 'time:', ctime(time())              # when was I run?
print 'prog:', program, '\n'              # what am I running?

try:                                             # get list of tests
    test_scripts = glob(sys.argv[2] + '/*.in')   # path passed in?
except IndexError: 
    test_scripts = glob('*.in')                  # filename expansion

fail = 0
for test in test_scripts:                        # for all input files:
    if exists(test + '.out'):                  
        os.rename(test + '.out', test + '.out.bkp')    # backup last run 

    try:    
        args = open(test + '.args').readline()[:-1]
    except: 
        args = ''           # no command-line args file
            
    # run test, compare results
    os.system('%s %s < %s > %s.out 2>&1' % (program, args, test, test))
    if not exists(test + '.out.bkp'):
        print 'PASSED:', test               # first time run
    else:
        os.system('diff %s.out %s.out.bkp > %s.diffs' % ((test,)*3) )
        if os.stat(test + '.diffs')[ST_SIZE] == 0:
            print 'PASSED:', test 
        else:
            fail = fail+1
            print 'FAILED:', test, '(see %s.diffs)' % test
    
print 'regtest done:', 
print (fail and `fail`+" error(s) found") or "no errors found."
sys.exit(fail != 0)              # 1 = errors, 0 = no errors (for callers)
