import os
import cenviron                         # get C module's methods

def putenv(name, value):                # redefine putenv
    os.environ[name] = value            # put in os.environ too
    cenviron.putenv(name, value)        # call custom C method

def getenv(name):
    value = cenviron.getenv(name)       # call C method
    if value != os.environ[name]:       # integrity check:
        os.environ[name] = value        # export to os.environ if
    return value                        # other libs called putenv
