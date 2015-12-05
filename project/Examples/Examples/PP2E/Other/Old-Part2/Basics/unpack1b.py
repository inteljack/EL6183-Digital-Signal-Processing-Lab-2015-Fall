#!/usr/local/bin/python

from sys import *                           # don't alter sys
marker = '::::::'
output = stdout                             # use explicit files

for line in stdin.readlines():              # for all input lines
    if line[:6] != marker:
        output.write(line)                  # write real lines
    else:
        output = open(line[6:-1], 'w')      # or make new output file
