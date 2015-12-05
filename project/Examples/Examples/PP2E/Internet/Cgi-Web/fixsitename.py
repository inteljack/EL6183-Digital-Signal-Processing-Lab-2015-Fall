#!/usr/bin/env python
###############################################################
# run this script in Cgi-Web dir after copying book web 
# examples to a new server--automatically changes all starship 
# server references in hyperlinks and form action tags to the 
# new server/site; warns about references that weren't changed
# (may need manual editing); note that starship references are 
# not usually needed or used--since browsers have memory, server 
# and path can usually be omitted from a URL in the prior page 
# if it lives at the same place (e.g., "file.cgi" is assumed to 
# be in the same server/path as a page that contains this name,
# with a real url like "http://lastserver/lastpath/file.cgi"),
# but a handful of URLs are fully specified in book examples;
# reuses the Visitor class developed in the system chapters,
# to visit and convert all files at and below current dir;
###############################################################

import os, string
from PP2E.PyTools.visitor import FileVisitor           # os.path.walk wrapper

listonly = 0
oldsite  = 'starship.python.net/~lutz'                 # server/rootdir in book
newsite  = 'XXXXXX/YYYYYY'                             # change to your site
warnof   = ['starship.python', 'lutz']                 # warn if left after fix
fixext   = ['.py', '.html', '.cgi']                    # file types to check

class FixStarship(FileVisitor):
    def __init__(self, listonly=0):                     # replace oldsite refs
        FileVisitor.__init__(self, listonly=listonly)   # in all web text files
        self.changed, self.warning = [], []             # need diff lists here
    def visitfile(self, fname):                         # or use find.find list
        FileVisitor.visitfile(self, fname)
        if self.listonly:
            return
        if os.path.splitext(fname)[1] in fixext:
            text = open(fname, 'r').read()
            if string.find(text, oldsite) != -1:    
                text = string.replace(text, oldsite, newsite)
                open(fname, 'w').write(text)
                self.changed.append(fname)
            for word in warnof:
                if string.find(text, word) != -1:
                    self.warning.append(fname); break

if __name__ == '__main__':
    # don't run auto if clicked
    go = raw_input('This script changes site in all web files; continue?') 
    if go != 'y':
        raw_input('Canceled - hit enter key')
    else:
        walker = FixStarship(listonly)
        walker.run()
        print 'Visited %d files and %d dirs' % (walker.fcount, walker.dcount)

        def showhistory(label, flist):
            print '\n%s in %d files:' % (label, len(flist))
            for fname in flist:
                print '=>', fname
        showhistory('Made changes', walker.changed)
        showhistory('Saw warnings', walker.warning)

        def edithistory(flist):
            for fname in flist:                      # your editor here
                os.system('vi ' + fname) 
        if raw_input('Edit changes?') == 'y':  edithistory(walker.changed)
        if raw_input('Edit warnings?') == 'y': edithistory(walker.warning)

