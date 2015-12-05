#!/usr/local/bin/python

from sys import argv, exit 
from textpak2 import pack, unpack         # reuse textpak2 stuff

menu = { 'pack':   pack,                  # interactive menu
         'unpack': unpack,                # 'key' : function
         'stop':   exit}                  # sys.exit on 'stop' 

def interact():
    while 1:
        for name in menu.keys():          # could do list.sort 
            print '\t' + name             # show options
        tool = raw_input('?')
        try:
            menu[tool]()                  # run function
        except KeyError:                  # let eof-error pass
            print 'what? - try again'     # key not found

if __name__ == '__main__':
    flags = {'-i':interact, '-p':pack, '-u':unpack}
    try:
        if len(argv) == 1:                          # no flags: interact
            interact()
        else:
            if flags.has_key(argv[1]):              # test key first
                flags[argv[1]]()                    # run function
            else:
                print 'usage error: -i | -p | -u'   # not found
    except EOFError: pass                           # ctrl-D exits anything
