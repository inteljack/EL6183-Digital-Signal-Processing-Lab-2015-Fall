import os, cenviron                         # get C module

class Environ:
    def getenv(self, name):                 # C module wrapper class
        return cenviron.getenv(name)        # delegate to C module
    def putenv(self, name, value): 
        cenviron.putenv(name, value)

class EnvSync(Environ):                     # extend by subclassing
    def putenv(self, name, value):
        os.environ[name] = value            # put in os.environ too
        Environ.putenv(self, name, value)   # do superclass putenv

    def getenv(self, name):
        value = Environ.getenv(self, name)  # do superclass getenv
        os.environ[name] = value            # integrity check
        return value

Env = EnvSync()                             # make one instance   
