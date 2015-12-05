#!/usr/bin/python
########################################################
# custom version of the now deprecated find module 
# in the standard library--import as "PyTools.find";
# equivalent to the original, but uses os.path.walk,
# has no support for pruning subdirs in the tree, and
# is instrumented to be runnable as a top-level script;
# results list sort differs slightly for some trees;
# exploits tuple unpacking in function argument lists;
########################################################

import fnmatch, os

def find(pattern, startdir=os.curdir):
    matches = []
    os.path.walk(startdir, findvisitor, (matches, pattern))
    matches.sort()
    return matches

def findvisitor((matches, pattern), thisdir, nameshere):
    for name in nameshere:
        if fnmatch.fnmatch(name, pattern):
            fullpath = os.path.join(thisdir, name)
            matches.append(fullpath)

if __name__ == '__main__':
    import sys
    namepattern, startdir = sys.argv[1], sys.argv[2]
    for name in find(namepattern, startdir): print name
