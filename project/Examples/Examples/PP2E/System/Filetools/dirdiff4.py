#!/bin/env python
########################################################
# use: python dirdiff.py <dir1-path> <dir2-path>
# compare two directories to find files that exist 
# in one but not the other;  this version uses the
# list.sort() method to precheck for equivalence;
########################################################

import os, dirdiff

def comparedirs(dir1, dir2):
    print 'Comparing', dir1, 'to', dir2
    files1 = os.listdir(dir1)
    files2 = os.listdir(dir2)
    files1.sort()
    files2.sort()
    if files1 == files2:
        print 'Directory lists are identical'
    else:
        unique1 = dirdiff.unique(files1, files2)
        unique2 = dirdiff.unique(files2, files1)
        dirdiff.reportdiffs(unique1, unique2, dir1, dir2)

if __name__ == '__main__':
    dir1, dir2 = dirdiff.getargs()
    comparedirs(dir1, dir2)

