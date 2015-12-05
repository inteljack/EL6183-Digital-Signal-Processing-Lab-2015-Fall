########################################################
# store items in a shelve, with file locks on writes;
# dbcommon assumes items are dictionaries (not here);
# chmod call assumes single file per shelve (e.g., gdbm);
# shelve allows simultaneous reads, but if any program
# is writing, no other reads or writes are allowed,
# so we obtain the lock before all load/store ops 
# need to chown to 0666, else only 'nobody' can write;
# this file doen't know about fcntl, but mutex doesn't
# know about cgi scripts--one of the 2 needs to add the
# path to FCNTL module for cgi script use only (here);
# we circumvent whatever locking mech the underlying
# dbm system may have, since we aquire alock on our own
# non-dbm file before attempting any dbm operation;
# allows multiple simultaneous readers, but writers 
# get exclusive access to the shelve; lock calls in  
# MutexCntl block and later resume callers if needed; 
########################################################

# cgi runs as 'nobody' without 
# the following default paths
import sys
sys.path.append('/usr/local/lib/python1.5/plat-linux2')

import dbcommon, shelve, os
from Mutex.mutexcntl import MutexCntl

class Dbase(MutexCntl, dbcommon.Dbase):             # mix mutex, dbcommon, mine
    def safe_writeItem(self, newdata):                         
        dbase = shelve.open(self.filename)          # got excl access: update
        dbase[self.makeKey()] = newdata             # save in shelve, safely
        dbase.close()
        os.chmod(self.filename, 0666)               # else others can't change

    def safe_readTable(self):
        reports = []                                # got shared access: load
        dbase = shelve.open(self.filename)          # no writers will be run
        for key in dbase.keys():                   
            reports.append(dbase[key])              # fetch data, safely
        dbase.close()
        return reports

    def writeItem(self, newdata):
        self.exclusiveAction(self.safe_writeItem, newdata)

    def readTable(self):
        return self.sharedAction(self.safe_readTable)

class DbaseErrata(Dbase):
    filename = 'DbaseShelve/errataDB'

class DbaseComment(Dbase):
    filename = 'DbaseShelve/commentDB'
