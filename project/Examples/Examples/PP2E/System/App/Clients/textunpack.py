#!/usr/local/bin/python
import sys
from textpack import marker                    # use common seperator key
mlen = len(marker)                             # file names after markers

for line in sys.stdin.readlines():             # for all input lines
    if line[:mlen] != marker:
        print line,                            # write real lines
    else:
        sys.stdout = open(line[mlen:-1], 'w')  # or make new output file
