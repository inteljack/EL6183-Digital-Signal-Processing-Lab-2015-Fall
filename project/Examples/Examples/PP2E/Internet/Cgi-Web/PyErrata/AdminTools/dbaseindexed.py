############################################################################
# add field index shelves to flat-file database mechanism;
# to optimize "index only" displays, use classes at end of this file;
# change browse, index, submit to use new loaders for "Index only" mode;
# minor nit: uses single lock file for all index shelve read/write ops;
# storing record copies instead of filenames in index shelves would be
# slightly faster (avoids opening flat files), but would take more space;
# falls back on original brute-force load logic for fields not indexed;
# shelve.open creates empty file if doesn't yet exist, so never fails;
# to start, create DbaseFilesIndex/{commentDB,errataDB}/indexes.lck;
############################################################################

import sys; sys.path.insert(0, '..')         # check admin parent dir first
from Mutex import mutexcntl                  # fcntl path okay: not 'nobody'
import dbfiles, shelve, pickle, string, sys

class Dbase(mutexcntl.MutexCntl, dbfiles.Dbase):
    def makeKey(self):
        return self.cachedKey
    def cacheKey(self):                                   # save filename
        self.cachedKey = dbfiles.Dbase.makeKey(self)      # need it here too
        return self.cachedKey

    def indexName(self, fieldname):
        return self.dirname + string.replace(fieldname, ' ', '-')

    def safeWriteIndex(self, fieldname, newdata, recfilename):
        index = shelve.open(self.indexName(fieldname))
        try:
            keyval  = newdata[fieldname]                  # recs have all fields
            reclist = index[keyval]                       # fetch, mod, rewrite
            reclist.append(recfilename)                   # add to current list
            index[keyval] = reclist
        except KeyError:
            index[keyval] = [recfilename]                 # add to new list

    def safeLoadKeysList(self, fieldname):
        if fieldname in self.indexfields:
            keys = shelve.open(self.indexName(fieldname)).keys()
            keys.sort()
        else:   
            keys, index = self.loadIndexedTable(fieldname)
        return keys

    def safeLoadByKey(self, fieldname, fieldvalue):
        if fieldname in self.indexfields:
            dbase = shelve.open(self.indexName(fieldname))
            try:
                index = dbase[fieldvalue]
                reports = []
                for filename in index:
                    pathname = self.dirname + filename + '.data'
                    reports.append(pickle.load(open(pathname, 'r')))
                return reports    
            except KeyError:
                return []
        else:
            key, index = self.loadIndexedTable(fieldname)
            try:
                return index[fieldvalue]
            except KeyError:
                return []

    # top-level interfaces (plus dbcommon and dbfiles)

    def writeItem(self, newdata):                 
        # extend to update indexes
        filename = self.cacheKey()
        dbfiles.Dbase.writeItem(self, newdata)
        for fieldname in self.indexfields:
            self.exclusiveAction(self.safeWriteIndex, 
                                 fieldname, newdata, filename)             

    def loadKeysList(self, fieldname):            
        # load field's keys list only
        return self.sharedAction(self.safeLoadKeysList, fieldname)

    def loadByKey(self, fieldname, fieldvalue):   
        # load matching recs lisy only
        return self.sharedAction(self.safeLoadByKey, fieldname, fieldvalue)

class DbaseErrata(Dbase):
    dirname     = 'DbaseFilesIndexed/errataDB/'
    filename    = dirname + 'indexes'
    indexfields = ['Submitter name', 'Submit date', 'Report state']

class DbaseComment(Dbase): 
    dirname     = 'DbaseFilesIndexed/commentDB/'
    filename    = dirname + 'indexes'
    indexfields = ['Submitter name', 'Report state']    # index just these

#
# self-test
#

if __name__ == '__main__':      
    import os      
    dbase = DbaseComment()
    os.system('rm %s*'        % dbase.dirname)          # empty dbase dir
    os.system('echo > %s.lck' % dbase.filename)         # init lock file
    
    # 3 recs; normally have submitter-email and description, not page 
    # submit-date and report-state are added auto by rec store method
    records = [{'Submitter name': 'Bob',   'Page': 38, 'Submit mode': ''},
               {'Submitter name': 'Brian', 'Page': 40, 'Submit mode': ''},
               {'Submitter name': 'Bob',   'Page': 42, 'Submit mode': 'email'}]
    for rec in records: dbase.storeItem(rec)

    dashes = '-'*80
    def one(item):
        print dashes; print item
    def all(list): 
        print dashes
        for x in list: print x

    one('old stuff')
    all(dbase.loadSortedTable('Submitter name'))              # load flat list
    all(dbase.loadIndexedTable('Submitter name'))             # load, grouped
   #one(dbase.loadIndexedTable('Submitter name')[0])
   #all(dbase.loadIndexedTable('Submitter name')[1]['Bob'])
   #all(dbase.loadIndexedTable('Submitter name')[1]['Brian'])

    one('new stuff')
    one(dbase.loadKeysList('Submitter name'))                 # bob, brian
    all(dbase.loadByKey('Submitter name', 'Bob'))             # two recs match
    all(dbase.loadByKey('Submitter name', 'Brian'))           # one rec mathces
    one(dbase.loadKeysList('Report state'))                   # all match
    all(dbase.loadByKey('Report state',   'Not yet verified')) 

    one('boundary cases')
    all(dbase.loadByKey('Submit mode',    ''))              # not indexed: load
    one(dbase.loadByKey('Report state',   'Nonesuch'))      # unknown value: []
    try:           dbase.loadByKey('Nonesuch',  'Nonesuch') # bad fields: exc
    except: print 'Nonesuch failed'

