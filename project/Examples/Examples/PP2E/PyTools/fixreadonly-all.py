#!/usr/bin/env python
###############################################################
# Use: python PyTools\fixreadonly-all.py 
# run this script in the top-level examples directory after
# copying all examples off the book's CD-ROM, to make all 
# files writeable again--by default, copying files off the 
# CD with Windows drag-and-drop (at least) creates them as 
# read-only on your hard drive; this script traverses entire 
# dir tree at and below the dir it is run in (all subdirs);
###############################################################

import os, string
from PP2E.PyTools.visitor import FileVisitor          # os.path.walk wrapper
listonly = 0

class FixReadOnly(FileVisitor):
    def __init__(self, listonly=0):    
        FileVisitor.__init__(self, listonly=listonly) 
    def visitDir(self, dname):
        FileVisitor.visitfile(self, fname)
        if self.listonly:
            return
        os.chmod(dname, 0777)
    def visitfile(self, fname):                     
        FileVisitor.visitfile(self, fname)
        if self.listonly:
            return
        os.chmod(fname, 0777)

if __name__ == '__main__':
    # don't run auto if clicked
    go = raw_input('This script makes all files writeable; continue?') 
    if go != 'y':
        raw_input('Canceled - hit enter key')
    else:
        walker = FixReadOnly(listonly)
        walker.run()
        print 'Visited %d files and %d dirs' % (walker.fcount, walker.dcount)
