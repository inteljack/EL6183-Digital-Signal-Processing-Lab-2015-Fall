################################################################
# Use: "python PyTools\visitor_replace.py fromStr toStr".
# does global search-and-replace in all files in a directory
# tree--replaces fromStr with toStr in all text files; this
# is powerful but dangerous!! visitor_edit.py runs an editor
# for you to verify and make changes, and so is much safer;
# use CollectVisitor to simply collect a list of matched files;
################################################################

import os, sys, string
from visitor import SearchVisitor
listonly = 0

class ReplaceVisitor(SearchVisitor):
    """ 
    change fromStr to toStr in files at and below startDir;
    files changed available in obj.changed list after a run
    """
    def __init__(self, fromStr, toStr, listonly=0):
        self.changed = []
        self.toStr   = toStr
        SearchVisitor.__init__(self, fromStr, listonly)
    def visitmatch(self, fname, text):
        fromStr, toStr = self.context, self.toStr
        text = string.replace(text, fromStr, toStr)
        open(fname, 'w').write(text)
        self.changed.append(fname)

if __name__  == '__main__':
    if raw_input('Are you sure?') == 'y':
        visitor = ReplaceVisitor(sys.argv[1], sys.argv[2], listonly)
        visitor.run(startDir='.')
        print 'Visited %d files'  % visitor.fcount
        print 'Changed %d files:' % len(visitor.changed)
        for fname in visitor.changed: print fname 

