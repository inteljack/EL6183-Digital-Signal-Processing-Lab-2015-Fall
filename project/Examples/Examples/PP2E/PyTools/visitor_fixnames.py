###############################################################
# recode fixnames_all.py name case fixer with the Visitor class
# note: "from fixnames_all import convertOne" doesn't help at 
# top-level of the fixnames class, since it is assumed to be a
# method and called with extra self argument (an exception);
###############################################################

from visitor import FileVisitor

class FixnamesVisitor(FileVisitor):
    """
    check filenames at and below startDir for uppercase
    """
    import fixnames_all
    def __init__(self, listonly=0):
        FileVisitor.__init__(self, listonly=listonly)
        self.ccount = 0
    def rename(self, pathname):
        if not self.listonly:
            convertflag = self.fixnames_all.convertOne(pathname)
            self.ccount = self.ccount + convertflag
    def visitdir(self, dirname):
        FileVisitor.visitdir(self, dirname)
        self.rename(dirname)
    def visitfile(self, filename):
        FileVisitor.visitfile(self, filename)
        self.rename(filename)

if __name__ == '__main__': 
    walker = FixnamesVisitor()
    walker.run()
    allnames = walker.fcount + walker.dcount
    print 'Converted %d files, visited %d' % (walker.ccount, allnames)
