#!/usr/local/bin/python
import sys 
from textpak2 import pack, unpack         # reuse textpak2 stuff

mymenu = { 'pack':   pack,                # interactive menu
           'unpack': unpack,              # not static class data
           'stop':   sys.exit}       

def Menu(menu):                        # a 'superclass'
    def run(obj, prompt='?'):          # a 'method'
        try:
            while 1:                         
                print '\n\tMENU...'
                obj['showOptions'](obj)    # call 'subclass' method
                command = raw_input(prompt)
                try:
                    flag = obj['runCommand'](obj, command)
                except (IndexError, KeyError):
                    print "what: '%s'?" % command 
                else:
                    if flag: break
        except EOFError: pass                

    obj = {}
    obj['menu'] = menu                 # assign 'data-member'
    obj['run']  = run                  # assign 'methods'
    return obj

def DictMenu(menu):                    # constructor
    def showOptions(obj):              # subclass methods
        options = obj['menu'].keys()   # nested functions
        options.sort()
        for cmd in options: print '\t\t' + cmd

    def runCommand(obj, cmd):
        return obj['menu'][cmd]()

    obj = Menu(menu)                   # call constructor
    obj['showOptions'] = showOptions   # assign methods
    obj['runCommand']  = runCommand    # can over-ride Menu keys
    return obj

#def ListMenu(menu):
#    ...etc.

if __name__ == '__main__': X = DictMenu(mymenu); X['run'](X)
