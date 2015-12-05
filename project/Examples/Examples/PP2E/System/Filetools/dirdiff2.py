#!/bin/env python
########################################################
# use: python dirdiff.py <dir1-path> <dir2-path>
# compare two directories to find files that exist 
# in one but not the other;  this version uses the
# glob.glob plus os.path.split to get file lists;
# glob retains directory paths and matched patterns;
########################################################

import glob, os, dirdiff

def comparedirs(dir1, dir2):
    print 'Comparing', dir1, 'to', dir2
    files1 = glob.glob(os.path.join(dir1, '*'))
    files2 = glob.glob(os.path.join(dir2, '*'))

    tail   = lambda x: os.path.split(x)[1]
    files1 = map(tail, files1)
    files2 = map(tail, files2)

    unique1 = dirdiff.unique(files1, files2)
    unique2 = dirdiff.unique(files2, files1)
    dirdiff.reportdiffs(unique1, unique2, dir1, dir2)

if __name__ == '__main__':
    dir1, dir2 = dirdiff.getargs()
    comparedirs(dir1, dir2)

