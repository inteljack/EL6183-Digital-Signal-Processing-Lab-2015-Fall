#!/usr/local/bin/python
import string, glob, os, sys
try:         
    srcdir = sys.argv[1]         # optional arg = directory
except:                          # scan C header, grep for constants
    srcdir = '.'
header = '/usr/local/include/Py/rename2.h'

for line in open(header, 'r').readlines():             # for all lines 
    if line[:7] == '#define':                          # starts with '#define'?
        oldname = string.split(line)[1]                # get word after #define
        print oldname
        for source in glob.glob(srcdir + '/*.[ch]'):   # for all ".c"/".h" files
            print source
            print os.popen('grep -w -n %s %s' % (oldname, source)).read()
print 'done.'
