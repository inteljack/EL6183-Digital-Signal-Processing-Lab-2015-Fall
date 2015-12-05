#! /usr/local/bin/python
import sys, regex
from string import strip

pattDefine = regex.compile(
    '^#[\t ]*define[\t ]+\([a-zA-Z0-9_]+\)[\t ]*')  

pattInclude = regex.compile(
    '^#[\t ]*include[\t ]+[<"]\([a-zA-Z0-9_/\.]+\)') 

def scan(file):
    count = 0
    while 1:                                   # scan line-by-line
        line = file.readline()
        if not line: break
        count = count + 1
        n = pattDefine.match(line)             # save length-of-match
        if n >= 0:
            name = pattDefine.group(1)         # substring for \(...\)
            body = line[n:]
            print count, name, '=', strip(body)
        elif pattInclude.match(line) >= 0:
            regs = pattInclude.regs            # start/stop indexes
            a, b = regs[1]                     # of first \(...\) group
            filename = line[a:b]               # slice out of line
            print count, 'include', filename

if len(sys.argv) == 1:
    scan(sys.stdin)                    # no args: read stdin
else:
    scan(open(sys.argv[1], 'r'))       # arg: input file name
