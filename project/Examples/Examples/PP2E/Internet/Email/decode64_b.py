#!/usr/bin/env python
#################################################
# Decode mail attachments sent in base64 form.
# This version tests the mimetools module.     
#################################################

import sys, mimetools

iname = 'part.txt'
oname = 'part.doc'

if len(sys.argv) > 1:
    iname, oname = sys.argv[1:]      # % python prog [iname oname]?

input  = open(iname, 'r')
output = open(oname, 'wb')
mimetools.decode(input, output, 'base64')     # or 'uuencode', etc.
print 'done'
