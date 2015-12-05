import sys
lines = sys.stdin.readlines()           # sort stdin input lines,
lines.sort()                            # send result to stdout
for line in lines: print line,          # for further processing
