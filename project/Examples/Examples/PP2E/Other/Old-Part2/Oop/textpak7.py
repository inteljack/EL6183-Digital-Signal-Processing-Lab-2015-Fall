#!/usr/local/bin/python

from menu1 import ListMenu                   # get menu interaction
from textpak2 import pack, unpack            # reuse textpak2 funcs

class TextPak(ListMenu): 
    menu = [ ('pack',   pack),               # ('key', function)
             ('unpack', unpack),            
             ('stop',   lambda:1) ] 

if __name__ == '__main__': TextPak().run()   # inherit from ListMenu
