###############################################################
# Use: "python PyTools\visitor_edit.py string".
# add auto-editor start up to SearchVisitor in an external
# component (subclass), not in-place changes; this version 
# automatically pops up an editor on each file containing the
# string as it traverses; you can also use editor='edit' or 
# 'notepad' on windows; 'vi' and 'edit' run in console window;
# editor=r'python Gui\TextEditor\textEditor.pyw' may work too;
# caveat: we might be able to make this smarter by sending
# a search command to go to the first match in some editors; 
###############################################################

import os, sys, string
from visitor import SearchVisitor
listonly = 0

class EditVisitor(SearchVisitor):
    """ 
    edit files at and below startDir having string
    """
    editor = 'vi'  # ymmv
    def visitmatch(self, fname, text):
        os.system('%s %s' % (self.editor, fname))

if __name__  == '__main__':
    visitor = EditVisitor(sys.argv[1], listonly)
    visitor.run('.')
    print 'Edited %d files, visited %d' % (visitor.scount, visitor.fcount)
