#!/usr/local/bin/python

from sys import argv, stdout              # use stdout explictly
marker = '::::::'

for name in argv[1:]:  
    input = open(name, 'r')
    stdout.write(marker + name + '\n')    # add an end-line
    stdout.write( input.read() )          # no end-line to strip
