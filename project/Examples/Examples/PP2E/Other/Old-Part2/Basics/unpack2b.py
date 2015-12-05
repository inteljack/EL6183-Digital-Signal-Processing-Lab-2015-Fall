#!/usr/local/bin/python 

import sys
marker = '::::::'

while 1:
    try: 
        line = raw_input()                      # sys.stdin implied
    except EOFError:                            # error at end-of-file
        break 
    if line[:6] != marker:
        print line                              # no end-line to strip
    else:
        sys.stdout = open(line[6:], 'w')        # no end-line to strip
