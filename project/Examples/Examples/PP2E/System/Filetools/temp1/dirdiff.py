#!/bin/env python
########################################################
# use: python dirdiff.py <dir1-path> <dir2-path>
# compare two directories to find files that exist 
# in one but not the other;  this version uses the
# os.listdir function and list difference;  note 
# that this script only checks filename, not file
# contents--see diffall.py for an extension that
# does the latter by comparing .read() results;
#
# alternatives (see dirdiff*.py, testdirdiffs.py)
# - use os.popen('ls...') or glob.glob + os.path.split 
#   to get file lists here (os.listdir returns file 
#   names without their directory paths):
# - use os.exists instead of file list differences; 
# - on unix systems we could do something similar by 
#   sort'ing and diff'ing ls shell command outputs;  
# - .sort the file lists and test if they are ==, to 
#   avoid the for loops below;
########################################################

import os, sys

def reportdiffs(unique1, unique2, dir1, dir2):
    if not (unique1 or unique2):
        print 'Directory lists are identical'
    else:
        if unique1:
            print 'Files unique to', dir1 
            for file in unique1: 
                print '...', file        
        if unique2:
            print 'Files unique to', dir2 
            for file in unique2: 
                print '...', file        

def unique(seq1, seq2):
    uniques = []                 # return items in seq1 only
    for item in seq1:
        if item not in seq2:
            uniques.append(item)
    return uniques

def comparedirs(dir1, dir2):
    print 'Comparing', dir1, 'to', dir2
    files1  = os.listdir(dir1)
    files2  = os.listdir(dir2)
    unique1 = unique(files1, files2)
    unique2 = unique(files2, files1)
    reportdiffs(unique1, unique2, dir1, dir2)

def getargs():
    try:
        dir1, dir2 = sys.argv[1:]     # 2 command-line agrs
    except:
        print 'Usage: dirdiff.py dir1 dir2'
        sys.exit(1)
    else:
        return (dir1, dir2)

if __name__ == '__main__':
    dir1, dir2 = getargs()
    comparedirs(dir1, dir2)

