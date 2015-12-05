#!/usr/local/bin/python

import textpak2                             # reuse textpak2 funcs
from interact import ListMenu               # get menu interaction

class TextPak(ListMenu): 
    def __init__(self):
        self.prompt = '>'
        self.menu = [ ('pack',   self.pack),        # ('key', method)
                      ('unpack', self.unpack),      # bound method objects
                      ('stop',   self.stop) ] 

    def pack(self):   return textpak2.pack()
    def unpack(self): return textpak2.unpack()      # local method defs
    def stop(self):   return 1

if __name__ == '__main__': TextPak().run()
