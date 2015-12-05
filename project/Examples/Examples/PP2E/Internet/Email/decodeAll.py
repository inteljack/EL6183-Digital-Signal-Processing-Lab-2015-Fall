#!/usr/bin/env python
#####################################################
# Decode all mail attachments sent in encoded form:
# base64, uu, etc. To use, copy entire mail message
# to mailfile and run:
#    % python ..\decodeAll.py mailfile
# which makes one or more mailfile.part* outputs.
#####################################################

import sys, mhlib
from types import *
iname = 'mailmessage.txt'

if len(sys.argv) == 3:
    iname, oname = sys.argv[1:]        # % python prog [iname [oname]?]?
elif len(sys.argv) == 2:
    iname = sys.argv[1]
    oname = iname + '.part'

def writeparts(part, oname):
    global partnum
    content = part.getbody()                   # decoded content or list
    if type(content) == ListType:              # multiparts: recur for each
        for subpart in content:
            writeparts(subpart, oname) 
    else:                                      # else single decoded part
        assert type(content) == StringType     # use filename if in headers
        print; print part.getparamnames()      # else make one with counter
        fmode = 'wb'
        fname = part.getparam('name')
        if not fname:
            fmode = 'w'
            fname = oname + str(partnum)
            if part.gettype() == 'text/plain':
                fname = fname + '.txt'
            elif part.gettype() == 'text/html':
                fname = fname + '.html'
        output = open(fname, fmode)            # mode must be 'wb' on windows
        print 'writing:', output.name          # for word doc files, not 'w'
        output.write(content)
        partnum = partnum + 1

partnum = 0
input   = open(iname, 'r')                     # open mail file
message = mhlib.Message('.', 0, input)         # folder, number args ignored
writeparts(message, oname)
print 'done: wrote %s parts' % partnum

