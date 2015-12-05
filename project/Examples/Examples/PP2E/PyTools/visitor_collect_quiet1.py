##############################################################
# Like visitor_collect, but avoid traversal status messages
##############################################################

import os, sys, string
from visitor import FileVisitor, SearchVisitor

class CollectVisitor(FileVisitor):
    """
    collect names of files containing a string, silently;
    """
    skipexts = SearchVisitor.skipexts
    def __init__(self, searchStr):
        self.matches = []
        self.context = searchStr
    def visitdir(self, dname): pass
    def visitfile(self, fname):
        if (os.path.splitext(fname)[1] not in self.skipexts and
            string.find(open(fname).read(), self.context) != -1):
            self.matches.append(fname)

if __name__  == '__main__':
    visitor = CollectVisitor(sys.argv[1])
    visitor.run(startDir='.')
    print 'Found these files:'
    for fname in visitor.matches: print fname 
