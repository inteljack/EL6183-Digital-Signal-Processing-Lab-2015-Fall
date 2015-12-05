import os
from cenviron import getenv, putenv       # get C module's methods

class EnvWrapper:                         # wrap in a Python class
    def __setattr__(self, name, value):
        os.environ[name] = value          # on writes: Env.name=value
        putenv(name, value)               # put in os.environ too

    def __getattr__(self, name):
        value = getenv(name)              # on reads: Env.name
        os.environ[name] = value          # integrity check
        return value

Env = EnvWrapper()                        # make one instance   
