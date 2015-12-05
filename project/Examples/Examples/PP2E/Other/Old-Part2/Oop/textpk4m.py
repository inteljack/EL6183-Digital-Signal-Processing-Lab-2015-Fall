#!/usr/local/bin/python

from sys import exit 
from textpak2 import pack, unpack         # reuse textpak2 tools
from menu0 import interact                # get the menu manager

menu = { 'pack':   pack,                  # interactive menu
         'unpack': unpack,                # 'key' : function
         'stop':   exit}                  # sys.exit on 'stop' 

if __name__ == '__main__': interact(menu)
