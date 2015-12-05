#!/usr/local/bin/python

import sys                      # load the system module
marker = '::::::'

for name in sys.argv[1:]:       # for all command arguments
    input = open(name, 'r')     # open the next input file
    print marker + name         # write a separator line
    print input.read(),         # and write the file's contents
