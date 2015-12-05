#!/usr/local/bin/python

from sys import *                         # system interfaces
from textpak1 import marker               # "textpak1.py" marker constant
mlen = len(marker)

def unpack_file(name):
    try:                                  # catch errors here
        input = open(name, 'r')
        unpack_stream(input)
    except:
        import sys
        print 'unpack error!', sys.exc_type, sys.exc_value

def unpack_stream(input, output=stdout):
    while 1:
        line = input.readline()
        if not line:                      # until end-of-file
            break                         # copy real lines
        elif line[:mlen] != marker:       # else, create file
            output.write(line)
        else:
            name = line[mlen:-1]
            print 'creating:', name
            output = open(name, 'w')

if __name__ == '__main__':  
    if len(argv) == 2:
        unpack_file(argv[1])
    else:
        print 'usage: unpack filename'; exit(1)
