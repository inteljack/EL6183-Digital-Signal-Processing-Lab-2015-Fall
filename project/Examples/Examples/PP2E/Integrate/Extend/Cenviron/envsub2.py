# this example was cut from the book

import os, cenviron                             # get C module

class Environ:
    def __getattr__(self, name):                # proxy class
        return getattr(cenviron, name)          # pass to C module

class EnvSync(Environ):                         # extend by wrapping
    def put(self, name, value):
        os.environ[name] = value                # put in os.environ too
        self.putenv(name, value)                # do C putenv

    def get(self, name):
        value = self.getenv(name)               # do C getenv
        os.environ[name] = value	        # synch up os.environ 
        return value

Env = EnvSync()		    		   
