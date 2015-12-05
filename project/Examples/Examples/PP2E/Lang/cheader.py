#! /usr/local/bin/python
import sys, re
from string import strip

pattDefine = re.compile(                               # compile to pattobj
    '^#[\t ]*define[\t ]+([a-zA-Z0-9_]+)[\t ]*(.*)')   # "# define xxx yyy..."

pattInclude = re.compile(
    '^#[\t ]*include[\t ]+[<"]([a-zA-Z0-9_/\.]+)')     # "# include <xxx>..."

def scan(file):
    count = 0
    while 1:                                     # scan line-by-line
        line = file.readline()
        if not line: break
        count = count + 1
        matchobj = pattDefine.match(line)        # None if match fails
        if matchobj:
            name = matchobj.group(1)             # substrings for (...) parts
            body = matchobj.group(2) 
            print count, 'defined', name, '=', strip(body)
            continue
        matchobj = pattInclude.match(line)
        if matchobj:
            start, stop = matchobj.span(1)       # start/stop indexes of (...) 
            filename = line[start:stop]          # slice out of line
            print count, 'include', filename     # same as matchobj.group(1)

if len(sys.argv) == 1:
    scan(sys.stdin)                    # no args: read stdin
else:
    scan(open(sys.argv[1], 'r'))       # arg: input file name
