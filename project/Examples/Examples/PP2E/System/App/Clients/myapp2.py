#!/usr/local/bin/python

from PP2E.System.App.apptools import *

def hello(): 
    print 'Hello world!'

def count():
    for i in range(eval( raw_input('Up to what? ') )):  
        print i, 
    print

def exit():
    print 'Bye-bye';  return 0

class MyApp(MenuDictApp):
    def __init__(self):
        MenuApp.__init__(self)
        self.symtab = {}               # local client data
        self.menu = {
          'hello' : hello,             # bound methods or funcs
          'count' : count,             # not static var--need self
          'args'  : self.showargs,     # or: lambda x=self: x.args,
          'env'   : self.showenv,
          'set'   : self.store,
          'get'   : self.fetch,
          'bye'   : exit
        }

    def showargs(self):
        return self.args

    def showenv(self):
        name = raw_input('Name (or <return>)? ')
        if name:
            print name, '="%s"' % self.getenv(name)     # not env[name]
        else:
            for (name, value) in self.env.items():
                print name, '=\t\t', value

    def store(self):
        name = raw_input('Name ? ')
        self.symtab[name] = raw_input('Value ? ')

    def fetch(self):
        try:
            return self.symtab[raw_input('Name ? ')]
        except:
            return 'Not found!'


if __name__ == '__main__':
    MyApp().main()

