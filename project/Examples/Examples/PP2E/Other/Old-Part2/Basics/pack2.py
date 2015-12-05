#!/usr/local/bin/python

from sys import *
from textpak1 import marker

def pack_file(name, output):  
    input = open(name, 'r')             
    output.write(marker + name + '\n')
    while 1:
        line = input.readline()                 # add 1 file 
        if not line: break                      # transfer line-by-line
        output.write(line)

def pack_all(outname, sources):	
    try:                                        # add all files
        output = open(outname, 'w')             # write explicit file 
    except:
        print 'error opening file'; exit(1)
    for name in sources:
        try:
            print 'packing:', name
            pack_file(name, output)
        except:
            print 'error processing:', name;  exit(1)

if __name__ == '__main__':   
    try:
        pack_all(argv[1], argv[2:])
    except IndexError:
        print 'usage: pack output src src...'; exit(1)
