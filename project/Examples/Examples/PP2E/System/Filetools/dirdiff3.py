#!/bin/env python
########################################################
# use: python dirdiff.py <dir1-path> <dir2-path>
# compare two directories to find files that exist 
# in one but not the other;  this version uses the
# os.listdir and os.exists, rathher than list diffs;
########################################################

import os, dirdiff
dir1, dir2 = dirdiff.getargs()

print 'Comparing', dir1, 'to', dir2
unique1 = []
for file in os.listdir(dir1):
    if not os.path.exists(os.path.join(dir2, file)): 
        unique1.append(file)

unique2 = []
for file in os.listdir(dir2):
    if not os.path.exists(os.path.join(dir1, file)): 
        unique2.append(file)

dirdiff.reportdiffs(unique1, unique2, dir1, dir2)

