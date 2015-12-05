#!/usr/local/bin/python
################################################################
# file unpackapp2.py
# add backup of prior file contents
# use method extension, versus a new flag to App.setOutput
# use 'try' versus existence testing
################################################################


import string
from PP2E.System.App.apptools import StreamApp
from textpack import marker


class UnpackApp(StreamApp):
    def start(self):
        self.endargs()          # ignore more -o's, etc.

    def run(self):
        mlen = len(marker)
        while 1:
            line = self.readline()
            if not line: 
                break
            elif line[:mlen] != marker:
                self.write(line)
            else:
                name = string.strip(line[mlen:])
                self.message('creating: ' + name)
                self.setOutput(name)

    def setOutput(self, name=None):
        import os
        try:
            os.rename(name, name + '.bkp')   
        except: pass
        StreamApp.setOutput(self, name)


if __name__ == '__main__':  UnpackApp().main()


