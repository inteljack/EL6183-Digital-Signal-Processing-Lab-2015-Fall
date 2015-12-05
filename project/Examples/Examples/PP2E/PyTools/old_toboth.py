########################################################
# THIS IS OLD CODE: SEE FIXEOLN FOR A BETTER SOLUTION.
# perform global search/replace for files in current 
# directory (only);  ex: python %X%\tools\todos.py *.*
# see the fixeoln*.py scripts for a better approach:
# this version only looks in one dir, and does a simple
# string replace--adds redundant \r's if run todos more
# than once!!; need binary open mode on dos, else reads
# auto drop \r from \r\n, and writes auto add \r to \n.
########################################################

import string, sys, glob             
debug = 0

def cmdpatts():
    if len(sys.argv) > 1:                   # filename patterns or names
        patts = sys.argv[1:]                # command-line or default
    else: 
        patts = ['*.py', '*.txt', '*.c', '*.h', 'make*']
    return patts

def convert(From='\r\n', To='\n', patts=None):
    patts = patts or cmdpatts()
    files = map(glob.glob, patts)           # glob always: * not applied on dos
    if debug: print files                   # though not really needed on linux

    for list in files:
        for fname in list:
            print fname
            old = open(fname, 'rb').read()         # dos needs 'b' to retain \r
            new = string.replace(old, From, To)    # same as split+join calls
            open(fname, 'wb').write(new)           # dos needs 'b' to avoid \r

