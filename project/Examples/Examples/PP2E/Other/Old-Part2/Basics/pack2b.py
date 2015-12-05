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

PackError = "Error packing files"                  # define exception string

def pack_all(outname, sources):	
    try:                         
        output = open(outname, 'w')    
    except:
        raise PackError, 'error opening file'      # raise, with message
    for name in sources:
        try:
            print 'packing:', name
            pack_file(name, output)
        except:
            raise PackError, 'error processing: ' + name

if __name__ == '__main__':   
    try:
        pack_all(argv[1], argv[2:])
    except IndexError:
        print 'usage: pack output src src...'; exit(1)
    except PackError, message:
        print PackError + '...', message; exit(1)
