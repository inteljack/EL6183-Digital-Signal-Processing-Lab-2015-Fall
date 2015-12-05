#################################################################
# Use: "python PyTools\visitor_collect.py searchstring".
# CollectVisitor simply collects a list of matched files, for
# display or later processing (e.g., replacement, auto-editing);
#################################################################

import os, sys, string
from visitor import SearchVisitor

class CollectVisitor(SearchVisitor):
    """
    collect names of files containing a string;
    run this and then fetch its obj.matches list
    """
    def __init__(self, searchstr, listonly=0):
        self.matches = []
        SearchVisitor.__init__(self, searchstr, listonly) 
    def visitmatch(self, fname, text):
        self.matches.append(fname)

if __name__  == '__main__':
    visitor = CollectVisitor(sys.argv[1])
    visitor.run(startDir='.')
    print 'Found these files:'
    for fname in visitor.matches: print fname 
