#########################################################
# Use: "python ..\..\PyTools\search_all.py string".
# search all files at and below current directory
# for a string; uses the os.path.walk interface,
# rather than doing a find to collect names first;
#########################################################

import os, sys, string
listonly = 0
skipexts = ['.gif', '.exe', '.pyc', '.o', '.a']        # ignore binary files

def visitfile(fname, searchKey):                       # for each non-dir file
    global fcount, vcount                              # search for string
    print vcount+1, '=>', fname                        # skip protected files
    try:
        if not listonly:
            if os.path.splitext(fname)[1] in skipexts:
                print 'Skipping', fname
            elif string.find(open(fname).read(), searchKey) != -1:
                raw_input('%s has %s' % (fname, searchKey))
                fcount = fcount + 1
    except: pass
    vcount = vcount + 1

def visitor(myData, directoryName, filesInDirectory):  # called for each dir 
    for fname in filesInDirectory:                     # do non-dir files here
        fpath = os.path.join(directoryName, fname)     # fnames have no dirpath
        if not os.path.isdir(fpath):                   # myData is searchKey
            visitfile(fpath, myData)
     
def searcher(startdir, searchkey):
    global fcount, vcount
    fcount = vcount = 0
    os.path.walk(startdir, visitor, searchkey)

if __name__ == '__main__':
    searcher('.', sys.argv[1])
    print 'Found in %d files, visited %d' % (fcount, vcount)
