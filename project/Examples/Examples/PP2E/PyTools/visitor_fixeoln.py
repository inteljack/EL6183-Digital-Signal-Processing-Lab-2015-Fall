##############################################################
# Use: "python visitor_fixeoln.py todos|tounix".
# recode fixeoln_all.py as a visitor subclass: this version
# uses os.path.walk, not find.find to collext all names first;
# limited but fast: if os.path.splitext(fname)[1] in patts:
##############################################################

import visitor, sys, fnmatch, os
from fixeoln_dir import patts
from fixeoln_one import convertEndlines

class EolnFixer(visitor.FileVisitor):
    def visitfile(self, fullname):                        # match on basename
        basename = os.path.basename(fullname)             # to make result same
        for patt in patts:                                # else visits fewer 
            if fnmatch.fnmatch(basename, patt):
                convertEndlines(self.context, fullname)
                self.fcount = self.fcount + 1             # could break here
                                                          # but results differ
if __name__ == '__main__':
    walker = EolnFixer(sys.argv[1])
    walker.run()
    print 'Files matched (converted or not):', walker.fcount

