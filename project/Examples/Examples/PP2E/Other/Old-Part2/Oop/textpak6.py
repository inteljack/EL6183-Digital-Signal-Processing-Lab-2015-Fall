#!/usr/local/bin/python

import sys 
from menu1 import DictMenu                # get menu interaction
from textpak2 import pack, unpack         # reuse textpak2 funcs

class TextPak(DictMenu):                     # subclass this menu
    menu = { 'pack':   pack,                 # my interactive menu
             'unpack': unpack,               # static class data
             'stop':   sys.exit}       

if __name__ == '__main__': TextPak().run()   # make one and run it
