############################################################
# Usage: "python cpall.py dir1 dir2".
# this version changes current directory along the way;
# the 'to' side is always the current dir, 'from' is a path 
############################################################

import os, sys
verbose = 0
dcount = fcount = 0

def cpall(dirFrom):
    global dcount, fcount
    for file in os.listdir(dirFrom):
        pathFrom = os.path.join(dirFrom, file)
        if not os.path.isdir(pathFrom):
            try:
                if verbose > 1: print 'copying file', pathFrom
                bytesFrom = open(pathFrom, 'rb').read()
                open(file, 'wb').write(bytesFrom)
                fcount = fcount+1
            except:
                print 'Error copying file', pathFrom, '--skipped'
                print sys.exc_type, sys.exc_value
        else:                                            
            if verbose: print 'copying dir', pathFrom
            try:
                os.mkdir(file)
            except:
                print 'Error creating dir', dirTo, '--skipped'
                print sys.exc_type, sys.exc_value
            else:
                os.chdir(file)
                cpall(pathFrom)
                os.chdir(os.pardir)                      
                dcount = dcount+1

if __name__ == '__main__':
    from cpall import getargs
    dirs = getargs()
    if dirs: 
        dirFrom, dirTo = dirs
        if not os.path.isabs(dirFrom):
            dirFrom = os.path.join(os.getcwd(), dirFrom)
        os.chdir(dirTo)
        cpall(dirFrom)
        print 'Copied', fcount, 'files,', dcount, 'directories'
