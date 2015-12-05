#!/usr/local/bin/python

from glob import glob
import pack2, unpack3	      
from interact import Interact

class TextPak(Interact):
    def __init__(self):
        self.prompt = "tool?  [pack, unpack, stop] "

    def evalCommand(self, name):
        if name == 'pack': 
            self.pack()
        elif name == 'unpack': 
            self.unpack()
        elif name == 'stop':
            return 1
        else:
            print 'what? - try again'

    def pack(self):
        output  = raw_input("output file name? ")
        pattern = raw_input("files to pack? ")  
        pack2.pack_all(output, glob(pattern))  

    def unpack(self): 
        unpack3.unpack_file( raw_input("input file name? ") )
            
if __name__ == '__main__': TextPak().run()
