#!/bin/env python
########################################################
# use: python dirdiff.py <dir1-path> <dir2-path>
# compare two directories to find files that exist 
# in one but not the other;  this version uses the
# os.listdir function and list difference, and simple
# top-level logic (not functions); 
########################################################

import os, sys

try:
    dir1, dir2 = sys.argv[1:]     # 2 command-line agrs
except:
    print 'Usage: dirdiff.py dir1 dir2'
    sys.exit(1)

print 'Comparing', dir1, 'to', dir2
files1 = os.listdir(dir1)
files2 = os.listdir(dir2)

unique1 = []
for file in files1:
    if file not in files2: 
        unique1.append(file)

unique2 = []
for file in files2:
    if file not in files1: 
        unique2.append(file)

if not (unique1 or unique2):
    print 'Directories lists are identical'
else:
    if unique1:
        print 'Files unique to', dir1 
        for file in unique1: 
            print '...', file        
    if unique2:
        print 'Files unique to', dir2 
        for file in unique2: 
            print '...', file        

