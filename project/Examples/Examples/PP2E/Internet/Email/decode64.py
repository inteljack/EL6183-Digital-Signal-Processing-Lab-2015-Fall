#!/usr/bin/env python
#################################################
# Decode mail attachments sent in base64 form.
# This version assumes that the base64 encoded 
# data has been extracted into a separate file.
# It doesn't understand mime headers or parts.
# uudecoding is similar (uu.decode(iname)),
# as is binhex decoding (binhex.hexbin(iname)).
# You can also do this with module mimetools:
# mimetools.decode(input, output, 'base64').
#################################################

import sys, base64

iname = 'part.txt'
oname = 'part.doc'

if len(sys.argv) > 1:
    iname, oname = sys.argv[1:]      # % python prog [iname oname]?

input  = open(iname, 'r')
output = open(oname, 'wb')           # need wb on windows for docs
base64.decode(input, output)         # this does most of the work
print 'done'
