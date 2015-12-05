###########################################################
# find and delete all "*.pyc" bytecode files at and below
# the directory where this script is run; this assumes a 
# Unix-like find command, and so is very non-portable; we
# could instead use the Python find module, or just walk 
# the directry trees with portable Python code; the find
# -exec option can apply a Python script to each file too;
###########################################################

import os, sys

if sys.platform[:3] == 'win':
    findcmd = r'c:\stuff\bin.mks\find . -name "*.pyc" -print'
else:
    findcmd = 'find . -name "*.pyc" -print'
print findcmd

count = 0
for file in os.popen(findcmd).readlines():        # for all file names
    count = count + 1                             # have \n at the end
    print str(file[:-1])
    os.remove(file[:-1])

print 'Removed %d .pyc files' % count

