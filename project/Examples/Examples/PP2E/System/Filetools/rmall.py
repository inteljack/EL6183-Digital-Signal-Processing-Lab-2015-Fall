#!/usr/bin/python
################################################################
# Use: "python rmall.py directoryPath directoryPath..."
# recursive directory tree deletion: removes all files and 
# directories at and below directoryPaths; recurs into subdirs
# and removes parent dir last, because os.rmdir requires that 
# directory is empty; like a Unix "rm -rf directoryPath" 
################################################################ 

import sys, os
fcount = dcount = 0

def rmall(dirPath):                             # delete dirPath and below
    global fcount, dcount
    namesHere = os.listdir(dirPath)
    for name in namesHere:                      # remove all contents first
        path = os.path.join(dirPath, name)
        if not os.path.isdir(path):             # remove simple files
            os.remove(path)
            fcount = fcount + 1
        else:                                   # recur to remove subdirs
            rmall(path)
    os.rmdir(dirPath)                           # remove now-empty dirPath
    dcount = dcount + 1

if __name__ == '__main__':
    import time
    start = time.time()
    for dname in sys.argv[1:]: rmall(dname)
    tottime = time.time() - start
    print 'Removed %d files and %d dirs in %s secs' % (fcount, dcount, tottime)
