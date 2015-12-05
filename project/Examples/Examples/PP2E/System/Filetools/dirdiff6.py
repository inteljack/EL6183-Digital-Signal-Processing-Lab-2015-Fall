#!/bin/env python
########################################################
# use: python dirdiff.py <dir1-path> <dir2-path>
# compare two directories to find files that exist 
# in one but not the other;  this version uses the
# os.popen() to run a shell command to get the file
# list; the popen result has no leading directory 
# paths, but .readlines retains the end-line char;
# note that an ls shell command may return files
# in a different sorted order than glob or listdir,
# which may make some tests register false failures;
# popen works only from a dos command-line on Windows;
########################################################

import glob, os, dirdiff

def comparedirs(dir1, dir2):
    print 'Comparing', dir1, 'to', dir2
    files1 = os.popen('ls %s' % dir1).readlines()
    files2 = os.popen('ls %s' % dir2).readlines()

    tail   = lambda x: x[:-1]
    files1 = map(tail, files1)
    files2 = map(tail, files2)

    unique1 = dirdiff.unique(files1, files2)
    unique2 = dirdiff.unique(files2, files1)
    dirdiff.reportdiffs(unique1, unique2, dir1, dir2)

if __name__ == '__main__':
    dir1, dir2 = dirdiff.getargs()
    comparedirs(dir1, dir2)

