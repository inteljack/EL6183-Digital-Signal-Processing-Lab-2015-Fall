#!/development/python-1.1/python
#file: myapp.py

from PP2E.System.App.apptools import *


def hello():
    print 'Hello world!'

def echo(x):
    return x


class Call:
    def __init__(self, func, *args):
        self.func = func		# func: func or bound-method
        self.left = args
    def __call__(self, *more):
        return apply(self.func, self.left + more)
    def call(self, *more):
        return apply(self, more)	# bound-method, like __call__


class MyApp(MenuDictApp):
    def start(self):                    # don't use __init__
        self.symtab = {}                # local client data
        self.menu = {
          'hello' : hello,        
          'count' : Call(self.count, 10),	
          'args'  : Call(echo, self.args),    
          'env'   : Call(self.showenv, 'USER').call,
          'set'   : self.store,
          'get'   : self.fetch,
          'bye'   : lambda: 0
        }

    def count(self, limit):
        for i in range(limit):  print i, 
        print

    def showenv(self, name):
        if name:
            print name, '= "%s"' % self.getenv(name)  
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

