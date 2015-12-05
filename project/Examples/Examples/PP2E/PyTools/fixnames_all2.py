###############################################################
# Use: "python ..\..\PyTools\fixnames_all2.py".
# same, but use the os.path.walk interface, not find.find;
# to make this work like the simple find version, puts of
# visiting directories until just before visiting their
# contents (find.find lists dir names before their contents);
# renaming dirs here can fail on case-sensitive platforms 
# too--walk keeps extending paths containing old dir names;
###############################################################

import os
listonly = 0
from fixnames_all import convertOne

def visitname(fname):
    global ccount, vcount
    print vcount+1, '=>', fname
    if not listonly:
        ccount = ccount + convertOne(fname)
    vcount = vcount + 1

def visitor(myData, directoryName, filesInDirectory):  # called for each dir 
    visitname(directoryName)                           # do dir we're in now,
    for fname in filesInDirectory:                     # and non-dir files here
        fpath = os.path.join(directoryName, fname)     # fnames have no dirpath
        if not os.path.isdir(fpath):
            visitname(fpath)
     
ccount = vcount = 0
os.path.walk('.', visitor, None)
print 'Converted %d files, visited %d' % (ccount, vcount)
