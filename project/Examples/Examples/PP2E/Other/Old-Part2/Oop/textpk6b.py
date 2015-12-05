#!/usr/local/bin/python

import sys 
from menu1 import DictMenu                # get menu interaction
from textpak2 import pack, unpack         # reuse textpak2 stuff

mymenu = { 'pack':   pack,                # interactive menu
           'unpack': unpack,              # not static class data
           'stop':   sys.exit}       

if __name__ == '__main__': 
    instance = DictMenu()                 # make a DictMenu directly
    instance.menu = mymenu                # assign instance member
    instance.run()
