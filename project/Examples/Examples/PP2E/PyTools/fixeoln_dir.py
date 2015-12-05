#########################################################
# Use: "python fixeoln_dir.py [tounix|todos] patterns?".
# convert end-lines in all the text files in the current
# directory (only: does not recurse to subdirectories). 
# Resuses converter in the single-file _one version.
#########################################################

import sys, glob
from fixeoln_one import convertEndlines
listonly = 0
patts = ['*.py', '*.pyw', '*.txt', '*.cgi', '*.html',    # text file names
         '*.c',  '*.cxx', '*.h',   '*.i',   '*.out',     # in this package
         'README*', 'makefile*', 'output*', '*.note']

if __name__ == '__main__':
    errmsg = 'Required first argument missing: "todos" or "tounix"'
    assert (len(sys.argv) >= 2 and sys.argv[1] in ['todos', 'tounix']), errmsg

    if len(sys.argv) > 2:                 # glob anyhow: '*' not applied on dos
        patts = sys.argv[2:]              # though not really needed on linux
    filelists = map(glob.glob, patts)     # name matches in this dir only 

    count = 0
    for list in filelists:
        for fname in list:
            if listonly:
                print count+1, '=>', fname
            else:
                convertEndlines(sys.argv[1], fname)
            count = count + 1

    print 'Visited %d files' % count
