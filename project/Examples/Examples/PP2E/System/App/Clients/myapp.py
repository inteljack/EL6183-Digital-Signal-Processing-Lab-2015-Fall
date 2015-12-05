#!/usr/local/bin/python

from PP2E.System.App.Kinds.interact import *

class MyApp(MenuDictApp):
    def __init__(self):		       # or: set menu in start()
        MenuDictApp.__init__(self)
        self.symtab = {}               # local client data
        self.menu = {
          'hello' : self.hello,        # bound methods or funcs
          'count' : self.count,	       # not static var--need self
          'args'  : self.showargs,     # or: lambda x=self: x.args,
          'env'   : self.showenv,
          'set'   : self.store,
          'get'   : self.fetch,
          'bye'   : self.exit
        }

    def hello(self):
        print 'Hello world!'

    def count(self):
        for i in range(eval( raw_input('Up to what? ') )):  print i, 
        print

    def showargs(self):
        return self.args

    def showenv(self):
        name = raw_input('Name (or <return>)? ')
        if name:
            print name, '= "%s"' % self.getenv(name)      # not env[name]
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

    def exit(self):
        print 'Bye-bye';  return 0


if __name__ == '__main__':
    MyApp().main()

