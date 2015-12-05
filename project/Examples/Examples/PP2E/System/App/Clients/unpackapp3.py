#!/usr/local/bin/python
################################################################
# file unpackapp3.py
# add backup of prior file contents (see unpackapp2.py)
# extend unpackapp, not app...
################################################################

from unpackapp import *

class UnpackAppBkp(UnpackApp):

    def setOutput(self, name=None):
        import os
        try:
            os.rename(name, name + '.bkp')   
        except: pass
        UnpackApp.setOutput(self, name)

if __name__ == '__main__':  UnpackAppBkp().main()

