#!/usr/local/bin/python

from textpak2 import pack, unpack
from menu0 import interact                  # get the menu manager

menu = [ ('pack',   pack),                  # 'key', function
         ('unpack', unpack),                # procedures return None
         ('stop',   lambda:1) ]             # return 1 to break loop

if __name__ == '__main__': interact(menu)
