#!/usr/local/bin/python
import sys, re, glob
from string import split

help_string = """
Usage options.
interactive:  % pygrep1.py
"""

def getargs():
    if len(sys.argv) == 1:
        return split(raw_input("patterns? >")), raw_input("files? >")
    else:
        try:
            return sys.argv[1], sys.argv[2]
        except:
            print help_string
            sys.exit(1)

def compile_patterns(patterns):
    res = []
    for pattstr in patterns:
        try:
            res.append(re.compile(pattstr))           # make re patt object 
        except:                                       # or use re.match 
            print 'pattern ignored:', pattstr 
    return res

def searcher(pattfile, srchfiles):
    patts = compile_patterns(pattfile)                  # compile for speed
    for file in glob.glob(srchfiles):                   # all matching files
        lineno = 1                                      # glob uses re too
        print '\n[%s]' % file
        for line in open(file, 'r').readlines():        # all lines in file
            for patt in patts:
                if patt.search(line):                   # try all patterns
                    print '%04d)' % lineno, line,       # match if not None
                    break
            lineno = lineno+1

if __name__ == '__main__': 
    apply(searcher, getargs())
