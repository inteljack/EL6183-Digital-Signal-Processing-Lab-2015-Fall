#!/usr/bin/python
################################################################
# Use: "python rmall2.py fileOrDirPath fileOrDirPath..."
# like rmall.py, alternative coding, files okay on cmd line
################################################################ 

import sys, os
fcount = dcount = 0

def rmone(pathName):
    global fcount, dcount
    if not os.path.isdir(pathName):               # remove simple files
        os.remove(pathName)
        fcount = fcount + 1
    else:                                         # recur to remove contents
        for name in os.listdir(pathName):
            rmone(os.path.join(pathName, name))
        os.rmdir(pathName)                        # remove now-empty dirPath
        dcount = dcount + 1

if __name__ == '__main__':
    import time
    start = time.time()
    for name in sys.argv[1:]: rmone(name)
    tottime = time.time() - start
    print 'Removed %d files and %d dirs in %s secs' % (fcount, dcount, tottime)
