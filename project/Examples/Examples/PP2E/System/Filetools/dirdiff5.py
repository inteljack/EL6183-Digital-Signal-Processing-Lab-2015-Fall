#!/bin/env python
########################################################
# use: python dirdiff.py <dir1-path> <dir2-path>
# compare two directories to find files that exist 
# in one but not the other;  this version uses an
# alternative coding for the unique() function;
########################################################

import os, dirdiff

def unique(seq1, seq2):
    uniques = seq1[:]    # copy seq1, remove all in seq2
    for item in seq2:
        try:
            uniques.remove(item)
        except ValueError:
            pass
    return uniques

def comparedirs(dir1, dir2):
    print 'Comparing', dir1, 'to', dir2
    files1  = os.listdir(dir1)
    files2  = os.listdir(dir2)
    unique1 = unique(files1, files2)
    unique2 = unique(files2, files1)
    dirdiff.reportdiffs(unique1, unique2, dir1, dir2)

if __name__ == '__main__':
    dir1, dir2 = dirdiff.getargs()
    comparedirs(dir1, dir2)

