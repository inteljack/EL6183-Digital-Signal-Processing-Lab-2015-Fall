#########################################################
# Usage: "python cpall-alt.py dir1 dir2".
# Recursive copy of a directory tree.  This version 
# gives an alternative coding structure; it also 
# creates the top-level from directory in the to
# directory (works like unix "cp -r dirFrom dirTo"),
# and so creates an extra directory level at dirTo.
#########################################################

import os, sys
verbose = 0
dcount = fcount = 0

def cpall(dirFrom, dirTo):
    global dcount, fcount
    if verbose: print 'copying dir', dirFrom, 'to', dirTo

    # make target directory
    leafDir = os.path.split(dirFrom)[1]            # get rightmost dir name
    dirTo   = os.path.join(dirTo, leafDir)         # create it inside dirTo
    try:
        os.mkdir(dirTo)
        dcount = dcount+1
    except:
        print 'Error creating', dirTo, '--skipped'
        print sys.exc_type, sys.exc_value
    else:
        # copy all files, subdirs
        for file in os.listdir(dirFrom):
            pathFrom = os.path.join(dirFrom, file)
            if os.path.isdir(pathFrom):
                cpall(pathFrom, dirTo)                     # recur into subdirs
            else:                                          # copy simple files 
                try:
                    pathTo = os.path.join(dirTo, file)
                    if verbose > 1: print 'copying', pathFrom, 'to', pathTo
                    bytesFrom = open(pathFrom, 'rb').read()
                    open(pathTo, 'wb').write(bytesFrom)
                    fcount = fcount+1
                except:
                    print 'Error copying', pathFrom, to, pathTo, '--skipped'
                    print sys.exc_type, sys.exc_value

if __name__ == '__main__':
    from cpall import getargs
    dirstuple = getargs()
    if dirstuple: 
        apply(cpall, dirstuple)
        print 'Copied', fcount, 'files,', dcount, 'directories'
