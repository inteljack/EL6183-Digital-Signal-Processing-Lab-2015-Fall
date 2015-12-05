#!/usr/bin/python
########################################################
# like verifyFiles.py, but do it to shelves; 
# caveats: we should really obtain a lock before shelve 
# updates here, and there is some scan logic redundancy
########################################################

import shelve
from verifycommon import markAsVerify, markAsReject

def analyse(dbase):
    for k in dbase.keys(): 
        data = dbase[k]
        if data['Report state'] == 'Not yet verified':
             print data
             if raw_input('Verify?') == 'y':
                 markAsVerify(data)
                 dbase[k] = data
             elif raw_input('Reject?') == 'y':
                 markAsReject(data)
                 dbase[k] = data
             elif raw_input('Delete?') == 'y':
                 del dbase[k]

print 'Errata...';    analyse(shelve.open('../DbaseShelve/errataDB'))
print 'Comments...';  analyse(shelve.open('../DbaseShelve/commentDB'))
