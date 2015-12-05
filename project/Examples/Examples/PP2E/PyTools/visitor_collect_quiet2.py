##############################################################
# Like visitor_collect, but avoid traversal status messages
##############################################################

import os, sys, string
from visitor import SearchVisitor

class NullOut:
    def write(self, line): pass

class CollectVisitor(SearchVisitor):
    """
    collect names of files containing a string, silently
    """
    def __init__(self, searchstr, listonly=0):
        self.matches = []
        self.saveout, sys.stdout = sys.stdout, NullOut()
        SearchVisitor.__init__(self, searchstr, listonly) 
    def __del__(self):
        sys.stdout = self.saveout
    def visitmatch(self, fname, text):
        self.matches.append(fname)

if __name__  == '__main__':
    visitor = CollectVisitor(sys.argv[1])
    visitor.run(startDir='.')
    matches = visitor.matches
    del visitor
    print 'Found these files:'
    for fname in matches: print fname 
