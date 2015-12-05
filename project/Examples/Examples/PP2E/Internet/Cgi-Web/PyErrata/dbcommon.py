##############################################################
# an abstract superclass with shared dbase access logic;
# stored records are assumed to be dictionaries (or other
# mapping), one key per field; dbase medium is undefined;
# subclasses: define writeItem and readTable as appropriate 
# for the underlying file medium--flat files, shelves, etc.
# subtlety: the 'Submit date' field added here could be kept
# as a tuple, and all sort/select logic will work; but since
# these values may be embedded in a url string, we don't want
# to convert from string to tuple using eval in index.cgi;
# for consistency and safety, we convert to strings here;
# if not for the url issue, tuples work fine as dict keys;
# must use fixed-width columns in time string to sort;
# this interface may be optimized in future releases;
##############################################################

import time, os

class Dbase:

    # store

    def makeKey(self):
        return "%s-%s" % (time.time(), os.getpid())    

    def writeItem(self, newdata):
        assert 0, 'writeItem must be customized'

    def storeItem(self, newdata):
        secsSinceEpoch          = time.time()
        timeTuple               = time.localtime(secsSinceEpoch)
        y_m_d_h_m_s             = timeTuple[:6]      
        newdata['Submit date']  = '%s/%02d/%02d, %02d:%02d:%02d' % y_m_d_h_m_s
        newdata['Report state'] = 'Not yet verified'
        self.writeItem(newdata)

    # load

    def readTable(self):
        assert 0, 'readTable must be customized'

    def loadSortedTable(self, field=None):            # returns a simple list
        reports = self.readTable()                    # ordered by field sort
        if field:
            reports.sort(lambda x, y, f=field: cmp(x[f], y[f]))
        return reports

    def loadIndexedTable(self, field):
        reports = self.readTable()
        index = {}
        for report in reports:
            try: 
                index[report[field]].append(report)   # group by field values
            except KeyError:
                index[report[field]] = [report]       # add first for this key
        keys = index.keys()
        keys.sort()                                   # sorted keys, groups dict
        return keys, index

