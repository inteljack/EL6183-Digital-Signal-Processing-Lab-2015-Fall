#!/usr/local/bin/python
import string, glob, os, sys
try:         
    srcdir = sys.argv[1]          # optional arg = directory | '-'
except:                           # scan C header, grep for constants
    srcdir = '.'
header = '/usr/local/include/Py/rename2.h'

oldnames = []
for line in open(header, 'r').readlines():        # scan by lines
    if line[:7] == '#define':                     # starts with '#define'?
        oldnames.append(string.split(line)[1])    # get word after #define

if srcdir == '-':                                 # "finder2.py -": dump names
    oldnames.sort()
    print string.joinfields(oldnames,'\n')
else:
    oldnames = string.joinfields(oldnames, '\n')      # put newlines between
    for source in glob.glob(srcdir + '/*.[ch]'):      # all ".c"/".h" files
        print source
        print os.popen('grep -w -n -F "%s" %s' % (oldnames, source)).read()
print 'done.'
