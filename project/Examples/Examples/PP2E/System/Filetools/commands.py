#!/usr/local/bin/python
from sys import argv
from scanfile import scanner

def processLine(line):                      # define a function
    if line[0] == '*':                      # applied to each line
        print "Ms.", line[1:-1]
    elif line[0] == '+': 
        print "Mr.", line[1:-1]             # strip 1st and last char
    else:
        raise 'unknown command', line       # raise an exception

filename = 'data.txt'
if len(argv) == 2: filename = argv[1]       # allow file name cmd arg
scanner(filename, processLine)              # start the scanner
