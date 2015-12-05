#!/usr/local/bin/python
import sys 
from textpak2 import pack, unpack           # reuse textpak2 stuff

mymenu = { 'pack':   pack,                  # interactive menu
           'unpack': unpack,                # not static class data
           'stop':   sys.exit}       

def Menu(menu):                             # a 'superclass'
    obj = {}                                # an 'instance'

    def run(prompt='?', self=obj):          # a 'method'
        try:                                # saves this call's "obj"
            while 1:                         
                print '\n\tMENU...'
                self['showOptions']()       # call 'subclass' method
                command = raw_input(prompt)
                try:
                    flag = self['runCommand'](command)
                except (IndexError, KeyError):
                    print "what: '%s'?" % command 
                else:
                    if flag: break
        except EOFError: pass                

    obj['menu'] = menu                      # assign 'data-member'
    obj['run']  = run                       # assign 'methods'
    return obj

def DictMenu(menu):                       # 'subclass' constructor
    obj = Menu(menu)                      # call constructor

    def showOptions(self=obj):            # subclass methods
        options = self['menu'].keys()     # nested functions
        options.sort()
        for cmd in options: print '\t\t' + cmd

    def runCommand(cmd, self=obj):
        return self['menu'][cmd]()

    obj['showOptions'] = showOptions      # assign methods
    obj['runCommand']  = runCommand       # can over-ride Menu keys
    return obj

if __name__ == '__main__': DictMenu(mymenu)['run']('>')
