#!/usr/local/bin/python

from sys import argv 
from string import upper, lower             # case converters
from textpak2 import pack, unpack           # reuse textpak2 stuff

menu = [ ('pack',   pack),                  # 'key', function
         ('unpack', unpack),                # procedures return None
         ('stop',   lambda:1) ]             # return 1 to break loop

def get_option():
    for (name, func) in menu:                  # show menu items
        print '\t%s)%s' % (upper(name[0]), name[1:])
    return lower(raw_input('?'))
 
def run_option(tool):
    for (name, func) in menu:
        if tool == name[0] or tool == name:    # matches menu key?
            return func()                      # run function
    print 'what? - try again'                  # name not found
    return None                                # not really needed...

def interact():
    while 1:
        tool = get_option()
        if run_option(tool): break             # func returned 'true'?

if __name__ == '__main__':
    flags = ['-i', interact, '-p', pack, '-u', unpack]
    try:
        if len(argv) == 1:                          # no flags: interact
            interact()
        else:
            try:
                option = flags.index(argv[1])       # search for flag
            except ValueError:
                print 'usage error: -i | -p | -u'   # not found
            else:
                flags[option+1]()                   # found: run function
    except EOFError: pass                           # ctrl-D exits anything
