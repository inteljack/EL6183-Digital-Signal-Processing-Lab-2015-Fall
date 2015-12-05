#!/usr/local/bin/python
import sys, regex, glob

help_string = """
Usage options.
interactive:  % pygrep1.py
command line: % pygrep1.py pattern-file search-files-pattern
"""

def handle_args():
    if len(sys.argv) == 1:
        return raw_input("patterns? >"), raw_input("files? >")
    else:
        try:
            return sys.argv[1], sys.argv[2]
        except:
            print help_string
            sys.exit(1)

def compile_patterns(pattfile):
    res = []
    for pattstr in open(pattfile, 'r').readlines():
        try:
            res.append(regex.compile(pattstr[:-1]))   # make regex object 
        except:                                       # strip end-of-line 
            print 'pattern ignored:', pattstr         # or use regex.match
    return res

def searcher(pattfile, srchfiles):
    patts = compile_patterns(pattfile)              # compile for speed
    for file in glob.glob(srchfiles):               # all matching files
        lineno = 1                                  # glob uses regex too
        print '\n[%s]' % file
        for line in open(file, 'r').readlines():        # all lines in file
            for patt in patts:
                if patt.search(line) >= 0:              # try all patterns
                    print '%04d)' % lineno, line,       # report line match
                    break
            lineno = lineno+1

if __name__ == '__main__': 
    from regex_syntax import *
    regex.set_syntax(RE_SYNTAX_EGREP)     # emacs is the default
    apply(searcher, handle_args())
