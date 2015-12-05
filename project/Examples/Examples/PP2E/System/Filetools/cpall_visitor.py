###########################################################
# Use: "python cpall_visitor.py fromDir toDir"
# cpall, but with the visitor classes and os.path.walk;
# the trick is to do string replacement of fromDir with
# toDir at the front of all the names walk passes in;
# assumes that the toDir does not exist initially;
###########################################################

import os
from PP2E.PyTools.visitor import FileVisitor
from cpall import cpfile, getargs
verbose = 1

class CpallVisitor(FileVisitor):
    def __init__(self, fromDir, toDir):
        self.fromDirLen = len(fromDir) + 1
        self.toDir      = toDir
        FileVisitor.__init__(self)
    def visitdir(self, dirpath):
        toPath = os.path.join(self.toDir, dirpath[self.fromDirLen:])
        if verbose: print 'd', dirpath, '=>', toPath
        os.mkdir(toPath)
        self.dcount = self.dcount + 1
    def visitfile(self, filepath):
        toPath = os.path.join(self.toDir, filepath[self.fromDirLen:])
        if verbose: print 'f', filepath, '=>', toPath
        cpfile(filepath, toPath)
        self.fcount = self.fcount + 1

if __name__ == '__main__':
    import sys, time
    fromDir, toDir = sys.argv[1:3]
    if len(sys.argv) > 3: verbose = 0 
    print 'Copying...'
    start = time.time()
    walker = CpallVisitor(fromDir, toDir)
    walker.run(startDir=fromDir)
    print 'Copied', walker.fcount, 'files,', walker.dcount, 'directories',
    print 'in', time.time() - start, 'seconds'
