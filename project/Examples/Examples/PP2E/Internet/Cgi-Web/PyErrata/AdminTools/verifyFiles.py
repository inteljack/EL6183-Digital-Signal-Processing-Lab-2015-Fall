#!/usr/bin/python
########################################################
# report state change and deletion operations;
# also need a tool for anonymously publishing reports
# sent by email that are of general interest--for now,
# they can be entered with the submit forms manually;
# this is text-based: the idea is that records can be
# browsed in the errata page first (sort by state to 
# see unverified ones), but an edit gui or web-based
# verification interface might be very useful to add;
########################################################

import glob, pickle, os
from verifycommon import markAsVerify, markAsReject

def analyse(kind):
    for file in glob.glob("../DbaseFiles/%s/*.data" % kind): 
        data = pickle.load(open(file, 'r'))
        if data['Report state'] == 'Not yet verified':
             print data
             if raw_input('Verify?') == 'y':
                 markAsVerify(data)
                 pickle.dump(data, open(file, 'w'))
             elif raw_input('Reject?') == 'y':
                 markAsReject(data)
                 pickle.dump(data, open(file, 'w'))
             elif raw_input('Delete?') == 'y':
                 os.remove(file)  # same as os.unlink
                
print 'Errata...';   analyse('errataDB')
print 'Comments...'; analyse('commentDB')
