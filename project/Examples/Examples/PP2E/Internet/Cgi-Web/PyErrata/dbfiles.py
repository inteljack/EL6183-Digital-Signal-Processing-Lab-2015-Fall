###############################################################
# store each item in a distinct flat file, pickled;
# dbcommon assumes records are dictionaries, but we don't here;
# chmod to 666 to allow admin access (else 'nobody' owns);
# subtlety: unique filenames prevent multiple writers for any
# given file, but it's still possible that a reader (browser)
# may try to read a file while it's being written, if the 
# glob.glob call returns the name of a created but still 
# incomplete file;  this is unlikely to happen (the file 
# would have to still be incomplete after the time from glob
# to unpickle has expired), but to avoid this risk, files are 
# created with a temp name, and only moved to the real name
# when they have been completely written and closed; 
# cgi scripts with persistent data are prone to parallel
# updates, since multiple cgi scripts may be running at once;
###############################################################

import dbcommon, pickle, glob, os

class Dbase(dbcommon.Dbase):
    def writeItem(self, newdata):
        name = self.dirname + self.makeKey()
        file = open(name, 'w') 
        pickle.dump(newdata, file)         # store in new file
        file.close()
        os.rename(name, name+'.data')      # visible to globs
        os.chmod(name+'.data', 0666)       # owned by 'nobody'

    def readTable(self):
        reports = []
        for filename in glob.glob(self.dirname + '*.data'):
            reports.append(pickle.load(open(filename, 'r')))
        return reports

class DbaseErrata(Dbase):
    dirname = 'DbaseFiles/errataDB/'

class DbaseComment(Dbase):
    dirname = 'DbaseFiles/commentDB/'

