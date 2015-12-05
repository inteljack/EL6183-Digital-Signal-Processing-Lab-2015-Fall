#############################################################
# Test: "python ..\..\PyTools\visitor.py testmask [string]".
# Uses OOP, classes, and subclasses to wrap some of the 
# details of using os.path.walk to walk and search; testmask 
# is an integer bitmask with 1 bit per available selftest;
# see also: visitor_edit/replace/find/fix*/.py subclasses,
# and the fixsitename.py client script in Internet\Cgi-Web;
#############################################################

import os, sys, string
listonly = 0

class FileVisitor:
    """
    visits all non-directory files below startDir;
    override visitfile to provide a file handler
    """
    def __init__(self, data=None, listonly=0):
        self.context  = data
        self.fcount   = 0
        self.dcount   = 0
        self.listonly = listonly
    def run(self, startDir=os.curdir):                  # default start='.'
        os.path.walk(startDir, self.visitor, None)    
    def visitor(self, data, dirName, filesInDir):       # called for each dir 
        self.visitdir(dirName)                          # do this dir first
        for fname in filesInDir:                        # do non-dir files 
            fpath = os.path.join(dirName, fname)        # fnames have no path
            if not os.path.isdir(fpath):
                self.visitfile(fpath)
    def visitdir(self, dirpath):                        # called for each dir
        self.dcount = self.dcount + 1                   # override or extend me
        print dirpath, '...'
    def visitfile(self, filepath):                      # called for each file
        self.fcount = self.fcount + 1                   # override or extend me
        print self.fcount, '=>', filepath               # default: print name

class SearchVisitor(FileVisitor):
    """ 
    search files at and below startDir for a string
    """
    skipexts = ['.gif', '.exe', '.pyc', '.o', '.a']     # skip binary files
    def __init__(self, key, listonly=0):
        FileVisitor.__init__(self, key, listonly)
        self.scount = 0
    def visitfile(self, fname):                         # test for a match
        FileVisitor.visitfile(self, fname)
        if not self.listonly:
            if os.path.splitext(fname)[1] in self.skipexts:
                print 'Skipping', fname
            else:
                text = open(fname).read()
                if string.find(text, self.context) != -1:
                    self.visitmatch(fname, text)
                    self.scount = self.scount + 1
    def visitmatch(self, fname, text):                     # process a match
        raw_input('%s has %s' % (fname, self.context))     # override me lower


# self-test logic
dolist   = 1
dosearch = 2    # 3=do list and search
donext   = 4    # when next test added

def selftest(testmask):
    if testmask & dolist:
       visitor = FileVisitor()
       visitor.run('.')
       print 'Visited %d files and %d dirs' % (visitor.fcount, visitor.dcount)

    if testmask & dosearch:   
       visitor = SearchVisitor(sys.argv[2], listonly)
       visitor.run('.')
       print 'Found in %d files, visited %d' % (visitor.scount, visitor.fcount)

if __name__ == '__main__':
    selftest(int(sys.argv[1]))    # e.g., 5 = dolist | dorename
