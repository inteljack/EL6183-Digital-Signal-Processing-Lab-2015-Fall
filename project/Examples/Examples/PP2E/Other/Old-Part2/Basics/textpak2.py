#!/usr/local/bin/python

marker = '::::::'

from glob import glob
from sys import argv
import pack2, unpack3                              # warning: circular!

def pack():
    output  = raw_input("output file name? ")
    pattern = raw_input("files to pack? ")         # expand filenames
    pack2.pack_all(output, glob(pattern))          # call as a function

def unpack(): 
    unpack3.unpack_file( raw_input("input file name? ") )

def interact():
    while 1:
        name = raw_input("tool?  [pack, unpack, stop] ")
        if name == 'pack': 
            pack()
        elif name == 'unpack': 
            unpack()
        elif name == 'stop':
            break
        else:
            print 'what? - try again'
            
if __name__ == '__main__':
    try:
        if len(argv) == 1:
            interact()
        else:
            if   argv[1] == '-i': interact()
            elif argv[1] == '-p': pack()
            elif argv[1] == '-u': unpack()
            else: print 'usage error'
    except EOFError: pass                         # ctrl-D exits anything
    print 'bye'
